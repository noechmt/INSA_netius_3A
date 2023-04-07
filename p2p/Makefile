CC=gcc
CFLAGS=-Wall
EXEC=lan_connect

all:$(EXEC)

lan_connect : lan_connect.o lan_connect_function.o lan_connect_sockets.o
		@$(CC) -o $@ $^ -pthread
ircerserv.o : lan_connect.h 

lan_connect_function : lan_connect_function.o
		@$(CC) -o $@ $^
lan_connect_function.o : lan_connect.h

lan_connect_sockets : lan_connect_sockets.o
		@$(CC) -o $@ $^
lan_connect_sockets.o : lan_connect.h

%.o: %.c 
		@$(CC) -o $@ -c $< $(CFLAGS)

clean: 
		rm -f *.o
		rm -f $(EXEC)