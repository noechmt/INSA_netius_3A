#include"SocketManager.h"

// Fonction a faire 
// Combien de joueurs ; Liste des IP ; Joueur se déconnecte ; 


void initOtherSocket(){
    listOtherSocket = calloc(1,sizeof(gameSocket));
    if (listOtherSocket == NULL ){
     stop(errorMessageInitList);
    }
}

gameSocket * initNewSocket( char * ipAddr , char * playerName , int port){
    gameSocket * newSocket ; 
    if ( (newSocket = calloc(1,sizeof(gameSocket))) == NULL ){
        stop(errorMessageInitNewSock);
    }
    bzero(newSocket->ip,IP_LENGTH +1);
    bzero(newSocket->playerName, NAME_LENGTH +1 );

    strncpy(newSocket->ip , ipAddr , IP_LENGTH );
    strncpy(newSocket->playerName , playerName , NAME_LENGTH );
    newSocket->port = port ;
    newSocket->next = NULL ;
    
    return newSocket ;
}

int getNbPlayer(){
    return NbPlayer ;
}

void addOtherSocket(char *ipAddr, char* playerName, int port ){
    if (ipAddr == NULL || playerName == NULL || port < 1000  ){
        stop(errorMessageBadArgs);
    }

    if (listOtherSocket == NULL){

        initOtherSocket();
        bzero(listOtherSocket->ip,IP_LENGTH +1);
        bzero(listOtherSocket->playerName, NAME_LENGTH +1 );

        strncpy(listOtherSocket->ip , ipAddr , IP_LENGTH );
        strncpy(listOtherSocket->playerName , playerName , NAME_LENGTH );
        listOtherSocket->port = port ;
        listOtherSocket->next = NULL ;

    }else{

        gameSocket* tmp = listOtherSocket ;

        while (tmp->next != NULL ){
            tmp = tmp->next ;
        }

        gameSocket *newSocket = initNewSocket(ipAddr,playerName,port);
        
        tmp->next = newSocket ;
    }
    NbPlayer ++ ;
}

void displayOtherSocket(){

    gameSocket * tmp = listOtherSocket ;
    printf("List other sockets : \n");
    while (tmp != NULL ){
        printf("IP : %s NAME : %s PORT : %d \n",tmp->ip,tmp->playerName,tmp->port);
        tmp = tmp->next;
    }
}

void supprOtherSocket(char * ip){

    if ( ip == NULL  ){
        printf(errorMessageBadArgs);
    }

    gameSocket * curr = listOtherSocket ; 
    gameSocket * prev = listOtherSocket ;
    while ( curr != NULL ){

        if ( strncmp(ip,curr->ip,IP_LENGTH) == 0 ){
            prev->next = curr->next ; 
            free(curr);
            NbPlayer -- ;
            return ;
        }
        prev = curr ;
        curr = curr->next ; 
    }
    
}


void flushOtherSocket(){
    gameSocket * curr = listOtherSocket ;
    gameSocket * next = listOtherSocket ;

    if (curr != NULL ){
        while ( curr->next != NULL ){
            next= curr->next ; 
            free(curr);
            NbPlayer -- ;
            curr = next;
        }
        free(curr);
        NbPlayer -- ;
    }
    listOtherSocket = NULL ;
}



int main(){
    
    addOtherSocket("192.168.24.144","Player1",1450);
    addOtherSocket("192.168.24.145","Player2",1451);
    addOtherSocket("192.168.24.146","Player3",1452);
    addOtherSocket("192.168.24.147","Player4",1453);
    displayOtherSocket();
    supprOtherSocket("192.168.24.149");
    displayOtherSocket();
    flushOtherSocket();
    printf("Players : %i\n",getNbPlayer());
    return 0 ;
}
