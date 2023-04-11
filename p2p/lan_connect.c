// C program to demonstrate peer to peer chat using Socket Programming
#include "lan_connect.h"
// INADDR_ANY
#define BUFSIZE 10000
char IP[4][25];
int PORT = 1234;
player *player_list = NULL;
char name[20];
int LOCAL_PORT = 1236;
int PORT_PYTHON = 1235;

void flushPlayerList()
{

    player *current_player = player_list;
    while (current_player != NULL)
    {
        struct player *next_player = current_player->next_player;
        free(current_player->ip_adress);
        free(current_player);
        current_player = next_player;
    }
}

int IQuit(const char *ip_address)
{
    printf("MyIp :-%s\n", ip_address);
    struct ifaddrs *ifaddr, *ifa;
    char host[NI_MAXHOST];
    int family, s, status;

    // Récupération de la liste des interfaces réseau de la machine
    if (getifaddrs(&ifaddr) == -1)
    {
        perror("getifaddrs");
        exit(EXIT_FAILURE);
    }

    // Parcours de la liste des interfaces réseau et comparaison des adresses IP
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next)
    {
        if (ifa->ifa_addr == NULL)
        {
            continue;
        }

        // Obtention du type d'adresse IP (IPv4 ou IPv6)
        family = ifa->ifa_addr->sa_family;

        // Ignorer les interfaces qui ne sont pas de type IPv4 ou IPv6
        if (family != AF_INET && family != AF_INET6)
        {
            continue;
        }

        // Conversion de l'adresse IP en chaîne de caractères
        s = getnameinfo(ifa->ifa_addr, (family == AF_INET) ? sizeof(struct sockaddr_in) : sizeof(struct sockaddr_in6), host, NI_MAXHOST, NULL, 0, NI_NUMERICHOST);
        if (s != 0)
        {
            printf("getnameinfo() failed: %s\n", gai_strerror(s));
            exit(EXIT_FAILURE);
        }

        // Comparaison de l'adresse IP avec l'adresse IP fournie en argument
        if (strcmp(ip_address, host) == 0)
        {
            // L'adresse IP fournie correspond à l'adresse IP de la machine locale
            freeifaddrs(ifaddr);
            printf("It's my Ip \n");
            return 1;
        }
    }

    // L'adresse IP fournie ne correspond pas à l'adresse IP de la machine locale
    freeifaddrs(ifaddr);
    printf("Not my Ip \n");
    return 0;
}

void print_ip_addresses()
{
    printf("Show PlayerList:\n");
    struct player *current = player_list;

    while (current != NULL)
    {
        printf("%s\n", current->ip_adress);
        current = current->next_player;
    }
}

void removePlayer(char *playerIp)
{
    player *tmp = player_list;
    player *prev = player_list;
    while (tmp != NULL)
    {

        if (strlen(tmp->ip_adress) == strlen(playerIp))
        {
            if (strncmp(tmp->ip_adress, playerIp, strlen(tmp->ip_adress)) == 0)
            {
                if (tmp == player_list)
                {
                    player_list = NULL;
                }
                prev->next_player = tmp->next_player;
                free(tmp);
                return;
            }
        }
        prev = tmp;
        tmp = tmp->next_player;
    }
}

int main(int argc, char **argv)
{
    /*char* msg = calloc(1024, 1);
    strncpy(msg, "coucou", strlen("coucou"));
    cesar_super_open_ssl(msg, 5);
    printf("%s\n", msg);
    de_cesar_super_open_ssl(msg, 5);
    printf("%s\n", msg);*/
    // initialisation du premier joueur
    int opt = 1;
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

    if (setsockopt(local_fd, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0)
    {
        perror("sock option problem ");
    }
    /*-----------------------------------------------------*/

    /*preparation de la connexion avec les autres*/
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    server_connect(server_fd);
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0)
    {
        perror("sock option problem ");
    }
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
    pthread_create(&tid, NULL, &receive_thread, &local_fd); // Creating thread to keep receiving message in real time
    receive_thread(&server_fd);
    close(server_fd);
    close(local_fd);
}

// Receiving messages on our port
void receiving(int fd)
{
    int client_socket = 6;
    struct sockaddr_in address;
    int valread;
    char *buffer = calloc(BUFSIZE, 1);
    int addrlen = sizeof(address);
    fd_set current_sockets, ready_sockets;

    // Initialize my current set
    FD_ZERO(&current_sockets);
    FD_SET(fd, &current_sockets);
    int k = 0;
    int opt = 1;
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
                    if ((client_socket = accept(fd, (struct sockaddr *)&address,
                                                (socklen_t *)&addrlen)) < 0)
                    {
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }
                    if (setsockopt(client_socket, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0)
                    {
                        perror("sock option problem ");
                    }
                    printf("client socket %i\n", client_socket);
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
                    if (count_check == 0 && strncmp("127.0.0.1", inet_ntoa(address.sin_addr), strlen(inet_ntoa(address.sin_addr))) != 0)
                    {
                        player *new_player = calloc(sizeof(player), 1);
                        initialize_player(new_player);
                        new_player->next_player = player_list;
                        player_list = new_player;
                        strncpy(player_list->ip_adress, inet_ntoa(address.sin_addr), strlen(inet_ntoa(address.sin_addr)));

                        player *share_ip = player_list;
                        share_ip = share_ip->next_player;
                        while (share_ip->next_player != NULL)
                        {
                            sending(player_list->ip_adress, 1234, share_ip->ip_adress);
                            share_ip = share_ip->next_player;
                        }
                        sending(player_list->ip_adress, 1234, "maj");
                    }
                    // FD_CLR(client_socket, &current_sockets);
                    //  close(client_socket);
                }
                else
                {
                    printf("socket fd in main : %i\n", i);
                    valread = recv(i, buffer, BUFSIZE, MSG_WAITALL);
                    /*Adding new player if the buffer is an IP adress*/
                    // buffer = de_cesar_super_open_ssl(buffer, 1);
                    close(i);
                    if (valread < 0)
                    {
                        perror("erreur de recv");
                    }
                    printf("message recu et transmis : %s\n", buffer);

                    if (strncmp(buffer, "192.168", strlen("192.168")) == 0)
                    {
                        player *new_player = calloc(sizeof(player), 1);
                        initialize_player(new_player);
                        new_player->next_player = player_list;
                        player_list = new_player;
                        strncpy(player_list->ip_adress, buffer, strlen(buffer));
                    }
                    else if (strncmp(buffer, "maj", strlen("maj")) == 0)
                    {
                        player *sending_to_all = player_list;
                        while (sending_to_all->next_player != NULL)
                        {
                            sending(sending_to_all->ip_adress, 1234, "new pelo");
                            sending_to_all = sending_to_all->next_player;
                        }
                    }
                    else if (strncmp(inet_ntoa(address.sin_addr), "127.0.0.1", strlen("127.0.0.1")) != 0)
                    {

                        if (strncmp(buffer, "{\"header\": \"quit\"", strlen("{\"header\": \"quit\"")) == 0)
                        {
                            printf("%s Has quit the game \n", inet_ntoa(address.sin_addr));
                            removePlayer(inet_ntoa(address.sin_addr));
                        }

                        sending_local(buffer);
                    }
                    else
                    {

                        player *send_players = player_list;
                        while (send_players->next_player != NULL && player_list != NULL)
                        {
                            printf("send to %s\n : ", send_players->ip_adress);
                            sending(send_players->ip_adress, 1234, buffer);
                            send_players = send_players->next_player;
                        }

                        if (strncmp(buffer, "{\"header\": \"quit\"", strlen("{\"header\": \"quit\"")) == 0)
                        {
                            printf("Good bye\n");
                            flushPlayerList(inet_ntoa(address.sin_addr));

                            return;
                        }
                    }

                    bzero(buffer, BUFSIZE);
                    close(client_socket);
                    FD_CLR(client_socket, &current_sockets);
                    FD_CLR(i, &current_sockets);
                }
            }
        }
        if (k == (FD_SETSIZE * 2))
            break;
    }
}
