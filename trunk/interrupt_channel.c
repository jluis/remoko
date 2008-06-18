#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/l2cap.h>

int main(int argc, char **argv)
{
    struct sockaddr_l2 loc_addr = { 0 }, rem_addr = { 0 };
    char buf[1024] = { 0 };
    int s, client, bytes_read,on, ret ;
    unsigned int opt = sizeof(rem_addr);

    // allocate socket
    s = socket(AF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP);

    //socket reuse
    on = 1;
    ret = setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));

    // bind socket to port 0x1001 of the first available 
    // bluetooth adapter
    loc_addr.l2_family = AF_BLUETOOTH;
    loc_addr.l2_bdaddr = *BDADDR_ANY;
    loc_addr.l2_psm = htobs(0x1013);


    if(bind(s, (struct sockaddr *)&loc_addr, sizeof(loc_addr)) < 0){ 

    	printf("erro no bind");

    }

    // put socket into listening mode
    listen(s, 1);

    printf("received [%d]\n", s);

    // accept one connection
    client = accept(s, (struct sockaddr *)&rem_addr, &opt);

    ba2str( &rem_addr.l2_bdaddr, buf );
    fprintf(stderr, "accepted connection from %s\n", buf);

    // read data from the client
    memset(buf, 0, sizeof(buf));
    bytes_read = recv(client, buf, sizeof(buf), 0);
    if( bytes_read > 0 ) {
        printf("received [%s]\n", buf);
    }

    // close connection
    close(client);
    close(s);
	return 0;
}
