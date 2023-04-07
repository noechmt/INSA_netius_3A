// C program to demonstrate peer to peer chat using Socket Programming
#include "lan_connect.h"
// INADDR_ANY

char IP[4][25];
int PORT = 1234;
player *player_list = NULL;
char name[20];
int LOCAL_PORT = 1236;
int PORT_PYTHON = 1235;

int main(int argc, char **argv)
{
    // initialisation du premier joueur
    player *first_player = calloc(sizeof(player), 1);
    initialize_player(first_player);
    first_player->next_player = player_list;
    player_list = first_player;
    // ---------------------------------------------------

    int server_fd, local_fd;

    /*connexion en local*/
    if ((local_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("local socket failed");
        close(local_fd);
        exit(EXIT_FAILURE);
    }
    local_connect(local_fd);
    /*-----------------------------------------------------*/

    /*preparation de la connexion avec les autres*/
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    server_connect(server_fd);
    /*-----------------------------------------------------*/
    so_linger(server_fd, local_fd);
    if (argc > 1)
    {
        player *new_first_player = calloc(sizeof(player), 1);
        initialize_player(new_first_player);
        new_first_player->next_player = player_list;
        player_list = new_first_player;
        strncpy(player_list->ip_adress, argv[1], strlen(argv[1]));
    }
    pthread_t tid;
    printf("Listening for other players... \n");
    pthread_create(&tid, NULL, &receive_thread, &server_fd); // Creating thread to keep receiving message in real time
    while (1)
    {
        receive_thread(&local_fd);
    }
    close(server_fd);
    close(local_fd);
}

// Receiving messages on our port
void receiving(int fd)
{
    struct sockaddr_in address;
    int valread;
    char *buffer = calloc(1024, 1);
    int addrlen = sizeof(address);
    fd_set current_sockets, ready_sockets;

    // Initialize my current set
    FD_ZERO(&current_sockets);
    FD_SET(fd, &current_sockets);
    int k = 0;
    while (1)
    {
        k++;
        ready_sockets = current_sockets;

        if (select(FD_SETSIZE, &ready_sockets, NULL, NULL, NULL) < 0)
        {
            perror("Error");
            exit(EXIT_FAILURE);
        }
        for (int i = 0; i < FD_SETSIZE; i++)
        {
            if (FD_ISSET(i, &ready_sockets))
            {
                int count_check = 0;

                if (i == fd)
                {
                    int client_socket;
                    if ((client_socket = accept(fd, (struct sockaddr *)&address,
                                                (socklen_t *)&addrlen)) < 0)
                    {
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }
                    FD_SET(client_socket, &current_sockets);
                    /*check if IP is in the list*/
                    player *add_player_list = player_list;
                    while (add_player_list->next_player != NULL)
                    {
                        if (strncmp(add_player_list->ip_adress, inet_ntoa(address.sin_addr), strlen(inet_ntoa(address.sin_addr))) == 0)
                        {
                            count_check++;
                        }
                        add_player_list = add_player_list->next_player;
                    }

                    /*adding ip to the list*/
                    if (count_check == 0 &&strncmp("127.0.0.1", inet_ntoa(address.sin_addr), strlen(inet_ntoa(address.sin_addr))) != 0)
                    {
                        player *new_player = calloc(sizeof(player), 1);
                        initialize_player(new_player);
                        new_player->next_player = player_list;
                        player_list = new_player;
                        strncpy(player_list->ip_adress, inet_ntoa(address.sin_addr), strlen(inet_ntoa(address.sin_addr)));

                        player* share_ip = player_list;
                        share_ip = share_ip->next_player;
                        while(share_ip->next_player != NULL){
                            sending(player_list->ip_adress, 1234, share_ip->ip_adress);
                            share_ip = share_ip->next_player;
                        }
                        sending(player_list->ip_adress, 1234, "maj");
                    }
                }
                else
                {
                    valread = recv(i, buffer, 1024, 0);
                    /*Adding new player if the buffer is an IP adress*/
                    
                    if (valread < 0)
                    {
                        perror("erreur de recv");
                    }
                    printf("message recu et transmis : %s\n", buffer);

                    if(strncmp(buffer, "192.168", strlen("192.168")) == 0){
                        player *new_player = calloc(sizeof(player), 1);
                        initialize_player(new_player);
                        new_player->next_player = player_list;
                        player_list = new_player;
                        strncpy(player_list->ip_adress, buffer, strlen(buffer));
                    }
                    else if(strncmp(buffer, "maj", strlen("maj")) == 0){
                        player *sending_to_all = player_list;
                        while(sending_to_all->next_player != NULL){
                            sending(sending_to_all->ip_adress, 1234, "new pelo");
                            sending_to_all = sending_to_all->next_player;
                        }
                    }
                    else if (strncmp(inet_ntoa(address.sin_addr), "127.0.0.1", strlen("127.0.0.1")) != 0)
                    {
                        sending_local(buffer);
                    }
                    else
                    {
                        player *send_players = player_list;
                        while (send_players->next_player != NULL)
                        {  
                            printf("send to %s\n : ", send_players->ip_adress);
                            sending(send_players->ip_adress, 1234, buffer);
                            send_players = send_players->next_player;
                        }
                    }
                    bzero(buffer, 1024);
                    FD_CLR(i, &current_sockets);
                }
            }
        }
        if (k == (FD_SETSIZE * 2))
            break;
    }
}