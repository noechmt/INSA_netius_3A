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

struct player {
    char* ip_adress;
    int fd;
    struct player *next_player;
};

typedef struct player player;

int sending(char *adress, int port, char *msg, int server_fd);
void local_connect(int local_fd);
/*void receiving_local(int fd);*/
void* receiving(void* fd_temp);
int sending_local(char *msg, int local_fd);
void initialize_player(player* play);
void so_linger(int server_fd, int local_fd);
void server_connect(int server_fd);
void flush_list(player *player);
