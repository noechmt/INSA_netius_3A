// C program to demonstrate peer to peer chat using Socket Programming
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/select.h>
#include <errno.h>
#include <string.h>
// INADDR_ANY
char name[20];
char* buffer_recup;

int sending(char *ip);
int serveur(char *ip, int PORT);
void receiving(int server_fd);
void* receive_thread(int server_fd);
int close_socket(int socket);
char *recup_4_python();
void recup_zero();

int close_socket(int socket)
{
    printf("socket closed\n");
    return close(socket);
}
int serveur(char *ip, int PORT)
{
    buffer_recup = calloc(1024, 1);
    bzero(buffer_recup, 1024);
    int server_fd;
    struct sockaddr_in address;

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    // Forcefully attaching socket to the port

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    // address.sin_addr.s_addr = inet_addr("192.168.206.185");
    address.sin_port = htons(1234);
    int yes = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1)
    {
        perror("setsockopt");
        pthread_exit(NULL);
    }
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 5) < 0)
    {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    return server_fd;
}

// Sending messages to port
int sending(char *ip1, char *data)
{
    while (1)
    {
        // Fetching port number
        int PORT_server = 1234;

        int sock = 0;
        struct sockaddr_in serv_addr;
        char buffer_send[1024] = {0};
        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
            printf("\n Socket creation error \n");
            close(sock);
            return -1;
        }

        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr.s_addr = inet_addr(ip1); // INADDR_ANY always gives an IP of 0.0.0.0
        serv_addr.sin_port = htons(PORT_server);
        //scanf("%s", buffer_send);
        strcpy(buffer_send, data)
        if (strncmp(buffer_send, "/quit", strlen("/quit")) == 0)
        {
            close(sock);
            return -1;
        }
        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
        {
            close(sock);
            return 0;
        }
        if (strlen(buffer_send) != 0)
        {
            if (send(sock, buffer_send, sizeof(buffer_send), 0) < 0)
            {
                perror("send error");
            }
            bzero(buffer_send, 1024);
        }
        printf("\nMessage sent\n");
        close(sock);
    }
}

// Calling receiving every 2 seconds
void* receive_thread(int server_fd)
{
    while (1)
    {
        sleep(0.5);
        receiving(server_fd);
    }
}

// Receiving messages on our port
void receiving(int server_fd)
{
    
    struct sockaddr_in address;
    int valread;
    char buffer[2000] = {0};
    int addrlen = sizeof(address);
    fd_set current_sockets, ready_sockets;
    bzero(buffer, 1024);
    // Initialize my current set
    FD_ZERO(&current_sockets);
    FD_SET(server_fd, &current_sockets);
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
                if (i == server_fd)
                {
                    int client_socket;

                    if ((client_socket = accept(server_fd, (struct sockaddr *)&address,
                                                (socklen_t *)&addrlen)) < 0)
                    {
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }
                    FD_SET(client_socket, &current_sockets);
                }
                else
                {
                    bzero(buffer, 1024);
                    valread = recv(i, buffer, sizeof(buffer), 0);
                    if (valread <= 0)
                    {
                        exit(EXIT_FAILURE);
                    }
                    bzero(buffer_recup, 1024);
                    strncpy(buffer_recup, buffer, strlen(buffer));
                    FD_CLR(i, &current_sockets);
                }
            }
        }
        if (k == (FD_SETSIZE * 2))
            break;
    }
}

char *recup_4_python()
{   
    if(strlen(buffer_recup) != 0){
        return buffer_recup;
    }
    else{
        return "None";
    }
}

void recup_zero(){
    bzero(buffer_recup, 1024);
}