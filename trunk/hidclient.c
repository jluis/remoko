/*
 *
 *  Copyright (C) 2008  Valerio Valerio <vdv100@gmail.com>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */



#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <malloc.h>
#include <syslog.h>
#include <signal.h>
#include <getopt.h>
#include <netinet/in.h>
#include <sys/types.h> 
#include <sys/poll.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>
#include <bluetooth/l2cap.h>
#include <bluetooth/sdp.h>
#include <bluetooth/hidp.h>


#define L2CAP_PSM_HIDP_CTRL 0x11
#define L2CAP_PSM_HIDP_INTR 0x13

uint8_t cls[3];

void error(char *msg)
{
    perror(msg);
    exit(1);
}

int create_socket()
{
	
     int sockfd, newsockfd, portno, clilen;
     char buffer[256];
     struct sockaddr_in serv_addr, cli_addr;
     int n;
    
     sockfd = socket(AF_INET, SOCK_STREAM, 0);

     if (sockfd < 0){
        error("ERROR opening socket");
     }

     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = 6543;
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);

     if (bind(sockfd, (struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0){
              error("ERROR on binding");
     }

    return sockfd;

}

/*From Bluez Utils 3.2*/

static int l2cap_listen(const bdaddr_t *bdaddr, unsigned short psm, int lm, int backlog)
{
	struct sockaddr_l2 addr;
	struct l2cap_options opts;
	int sk;

	if ((sk = socket(PF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP)) < 0)
		return -1;

	memset(&addr, 0, sizeof(addr));
	addr.l2_family = AF_BLUETOOTH;
	bacpy(&addr.l2_bdaddr, bdaddr);
	addr.l2_psm = htobs(psm);

	if (bind(sk, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
		close(sk);
		return -1;
	}

	setsockopt(sk, SOL_L2CAP, L2CAP_LM, &lm, sizeof(lm));

	memset(&opts, 0, sizeof(opts));
	opts.imtu = HIDP_DEFAULT_MTU;
	opts.omtu = HIDP_DEFAULT_MTU;
	opts.flush_to = 0xffff;

	setsockopt(sk, SOL_L2CAP, L2CAP_OPTIONS, &opts, sizeof(opts));

	if (listen(sk, backlog) < 0) {
		close(sk);
		return -1;
	}

	return sk;
}

/*From Bluez Utils 3.2*/

static int l2cap_accept(int sk, bdaddr_t *bdaddr)
{
	struct sockaddr_l2 addr;
	socklen_t addrlen;
	int nsk;

	memset(&addr, 0, sizeof(addr));
	addrlen = sizeof(addr);

	if ((nsk = accept(sk, (struct sockaddr *) &addr, &addrlen)) < 0)
		return -1;

	if (bdaddr)
		bacpy(bdaddr, &addr.l2_bdaddr);

	return nsk;
}

static uint8_t* get_device_class(int hdev)
{
	static char dev_class[3];
	int s = hci_open_dev(hdev);

	if (s < 0) {
		fprintf(stderr, "Can't open device hci%d: %s (%d)\n",
						hdev, strerror(errno), errno);
		exit(1);
	}
	
	if (hci_read_class_of_dev(s, cls, 1000) < 0) {
		fprintf(stderr, "Can't read class of device on hci%d: %s (%d)\n",
						hdev, strerror(errno), errno);
		exit(1);
	}
	
	return cls;

}

static void set_device_class(int hdev, char* class)
{

	int s = hci_open_dev(hdev);

	uint32_t cod = strtoul(class, NULL, 16);
	if (hci_write_class_of_dev(s, cod, 2000) < 0) {
		fprintf(stderr, "Can't write local class of device on hci%d: %s (%d)\n",
						hdev, strerror(errno), errno);
		exit(1);
	}

}

static void send_event(int is, int modifiers, int val)
{

        unsigned char th[10];
	
	th[0] = 0xa1;
	th[1] = 0x01;
	th[2] = modifiers; //1 -left control ,2 - left shift, 4 left alt,5- ctrl+ alt (01 + 04) 8 - left gui, 16 - right control, 32 - right sift, 64 - right alt, 128 - right gui
	th[3] = 0x00;
	th[4] = val; // the key code
	th[5] = 0x00;
	th[6] = 0x00;
	th[7] = 0x00;
	th[8] = 0x00;
	th[9] = 0x00;
	

	write(is, th, sizeof(th));
	//printf("%d\n", th[4]);
	th[4] = 0x00;
	write(is, th, sizeof(th));
}

static void send_mouse_event(int is, int btn, int mov_x, int mov_y, int whell)
{

        unsigned char th[10];
	
	th[0] = 0xa1;
	th[1] = 0x02;
	th[2] = btn; // 0x01 - left, 0x02 - right, 0x04 - middle, 0x08 - side, 0x10 - extra
	th[3] = mov_x;
	th[4] = mov_y; // the key code
	th[5] = whell;
	th[6] = 0x00;
	th[7] = 0x00;
	th[8] = 0x00;
	th[9] = 0x00;
	

	write(is, th, sizeof(th));
	//printf("%d\n", th[4]);
	//th[4] = 0x00;
	//write(is, th, sizeof(th));
}




int main(int argc, char *argv[])
{
	int opt, ctl, csk, isk,cs,is,i,n,sockfd, newsockfd, clilen, client_addr;
	bdaddr_t bdaddr, dev;
	char addr[18];
	int bytes_read,lm = 0;
	char buf[1024] = { 0 };
	char buf2[1024] = { 0 };
	char val[4];
	int hdev = 0;
	uint8_t* dev_class;
	uint8_t* dev_class2;
	char default_class[8];
	unsigned char th[10];
     	char buffer[256];
    	char event[3];
     	char modifiers[3];
     	char key_value[3];
     	char btn[3];
     	char mov_x[4];
     	char mov_y[4];
     	char whell[4];
	char chk[2];
        char chk2[2];
     	struct sockaddr_in serv_addr, cli_addr;
	int client_len = 20;
     
	
	dev_class = get_device_class(0);
	printf("0x%02x%02x%02x\n", dev_class[2], dev_class[1], dev_class[0]);

	sprintf(default_class,"0x%02x%02x%02x\n", dev_class[2], dev_class[1], dev_class[0]);
	printf("%s", default_class);
	
	set_device_class(hdev, "0x0005c0");

	dev_class2 = get_device_class(0);
	printf("Device Class changed to: 0x%02x%02x%02x\n", dev_class2[2], dev_class2[1], dev_class2[0]);
	
	
	csk = l2cap_listen(BDADDR_ANY, L2CAP_PSM_HIDP_CTRL, lm, 10);
		if (csk < 0) {
			perror("Can't listen on HID control channel");
			close(ctl);
			exit(1);
		}

	isk = l2cap_listen(BDADDR_ANY, L2CAP_PSM_HIDP_INTR, lm, 10);
		if (isk < 0) {
			perror("Can't listen on HID interrupt channel");
			close(ctl);
			close(csk);
			exit(1);
		}
		
	cs = l2cap_accept(csk, NULL);
	
	is = l2cap_accept(isk, NULL);
	

	sockfd = create_socket();
     

     	listen(sockfd,5);
     	clilen = sizeof(cli_addr);
     	newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);

     	if (newsockfd < 0){
		error("ERROR on accept");
    	}

	while (1){
	     
		bzero(buffer,256);
		n = recv(newsockfd,buffer,255,0);

		if (n < 0){
		 error("ERROR reading from socket");
		}

			printf("The message: %s\n",buffer);
			n = write(newsockfd,"Message received",17);
			strncpy(event, &buffer[0],2);
			event[2] = '\0';
			printf("event: %s\n", event);

		if (n < 0){
			error("ERROR writing to socket");
		}

		if (strcmp(event,"01") == 0){
			printf("keyboard\n");

			strncpy(modifiers, &buffer[3],2);
			modifiers[2] = '\0';
			printf("modifiers: %s\n", modifiers);

			strncpy(key_value, &buffer[6],2);
			key_value[2] = '\0';
			printf("key_value: %s\n", key_value);

			send_event(is,atoi(modifiers),atoi(key_value));

		}
		else if (strcmp(event, "02") == 0){
			printf("mouse\n");

			strncpy(btn, &buffer[3],2);
			btn[2] = '\0';
			printf("btn: %s\n", btn);

			strncpy(chk, &buffer[6],1);
			chk[1] = '\0';
			printf("gh %s\n", chk);

			strncpy(chk2, &buffer[9],1);
			chk2[1] = '\0';
			printf("gh %s\n", chk2);

			if (strcmp(chk,"-") == 0){

				strncpy(mov_x, &buffer[6],3);
				mov_x[3] = '\0';
				printf("mov_x: %s\n", mov_x);

				bzero(chk2,sizeof(chk2));
				strncpy(chk2, &buffer[10],1);
				chk2[1] = '\0';
				printf("gh %s\n", chk2);
				if(strcmp(chk2,"-") == 0){

					strncpy(mov_y, &buffer[10],3);
					mov_y[3] = '\0';
					printf("mov_y: %s\n", mov_y);

					strncpy(whell, &buffer[14],2);
					whell[2] = '\0';
					printf("whell: %s\n", whell);
				}
				else{
					strncpy(mov_y, &buffer[10],2);
					mov_y[2] = '\0';
					printf("mov_y: %s\n", mov_y);

					strncpy(whell, &buffer[13],2);
					whell[2] = '\0';
					printf("whell: %s\n", whell);
				}
							
			}
			
			else if(strcmp(chk2,"-") == 0){	
							
				strncpy(mov_x, &buffer[6],2);
				mov_x[2] = '\0';
				printf("mov_x: %s\n", mov_x);

				strncpy(mov_y, &buffer[9],3);
				mov_y[3] = '\0';
				printf("mov_y: %s\n", mov_y);

				strncpy(whell, &buffer[13],2);
				whell[2] = '\0';
				printf("whell: %s\n", whell);
			}

			else{
				

				strncpy(mov_x, &buffer[6],2);
				mov_x[2] = '\0';
				printf("mov_x: %s\n", mov_x);

				strncpy(mov_y, &buffer[9],2);
				mov_y[2] = '\0';
				printf("mov_y: %s\n", mov_y);

				strncpy(whell, &buffer[12],2);
				whell[2] = '\0';
				printf("whell: %s\n", whell);
			}
			send_mouse_event(is,atoi(btn),atoi(mov_x),atoi(mov_y),atoi(whell));
		}
		else{

			if(!strcmp (buffer, "quit")){

				set_device_class(hdev, default_class);
				printf("Device class changed to: %s\n", default_class);
				close(cs);
				close(is);
				close(sockfd);
				close(newsockfd);
				exit(1);
				
			}
			printf("invalid\n");
		}
     }
     close(cs);
     close(is);
     close(sockfd);
     close(newsockfd);

		/*
		memset(val,0, sizeof(val));

		if(scanf("%s", val)){
			
			if(!strcmp (val, "quit")){

				set_device_class(hdev, default_class);
				printf("Device class changed to: %s\n", default_class);
				close(cs);
				close(is);
				exit(1);
				
			}
			
				getchar();
				send_event(is, 0, atoi(val));
				
		}*/
	
}
