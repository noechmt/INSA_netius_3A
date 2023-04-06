#include<stdlib.h>
#include<stdio.h>
#include<errno.h>
#include<string.h>
#include<strings.h>

#define DATA_LENGTH 1024
#define PORT_DEFAULT 10000
#define IP_LENGTH 17
#define NAME_LENGTH 50
#define PORT_LISTENER 1234

typedef struct{

    int header ;
    char data[DATA_LENGTH +1 ];


}netiusPackage;

struct gameSocket{

    char ip[IP_LENGTH +1 ] ;
    char playerName[NAME_LENGTH +1 ];
    int port ; 
    struct gameSocket * next ;


};

typedef struct gameSocket gameSocket ;


gameSocket * listOtherSocket ;
int NbPlayer = 0 ;
// System
void stop ( char * error_msg ){
    perror(error_msg);
    exit(1);
}

// Liste message d'erreur 
char errorMessageInitList[] = "Can't initialise listOtherSocket\n";
char errorMessageBadArgs[] = "Bad arguments\n";
char errorMessageInitNewSock[] = "Can't initialise new socket\n";

// Liste chainé

int getNbPlayer(); // Avoir le nombre de joueurs 
void initOtherSocket();
void addOtherSocket(char *ipAddr, char* playerName, int port );
void supprOtherSocket(char * ip); // Supprimer une socket 
void displayOtherSocket(); // Afficher toutes les sockets connectées
gameSocket * initNewSocket( char * ipAddr , char * playerName , int port); // Créer une nouvelle socket
void flushOtherSocket(); // Supprime tout 
void sendData(int header , char * data , int lengthData); // Envoie les données à tout le monde 

void initialisation(); // Ouverture socket, forck ou select 
void attempConnection(); // Procedure de connection à une partie 
void expectConnection(); // Atente d'une tentative de connection 
void disconnection(); // Déconnection

void sendNewMapOhter();
void receiveDataFromOther();
