CC = gcc

EXECUTABLES = hidclient

all: $(EXECUTABLES)

run:
	sudo ./hidclient



hidclient.o: hidclient.c


clean:
	rm -f core *.o $(EXECUTABLES) a.out

.SUFFIXES: .c .o
.c.o:
	$(CC) $(CFLAGS) -c $*.c

hidclient: hidclient.o
	$(CC) $(CFLAGS) -o hidclient hidclient.o -lbluetooth
