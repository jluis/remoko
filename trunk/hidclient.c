
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <malloc.h>
#include <syslog.h>
#include <signal.h>
#include <getopt.h>
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

int main()
{
	int opt, ctl, csk, isk,cs,is,i;
	bdaddr_t bdaddr, dev;
	char addr[18];
	int bytes_read,lm = 0;
	char buf[1024] = { 0 };
	char buf2[1024] = { 0 };
	
	unsigned char th[12];
	unsigned char cenas[1];
	unsigned char th2[12];
	
	/*ba2str(&bdaddr, addr);*/
/*
	ctl = socket(AF_BLUETOOTH, SOCK_RAW, BTPROTO_HIDP);
	if (ctl < 0) {
		perror("Can't open HIDP control socket");
		exit(1);
	}
	
	*/
	
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
	
	sleep(5);
	//write(cs, th, 1);
	//bzero(th, 12);
	
	th[0] = 0xa1;
	th[1] = 0x01;
	th[2] = 0x00; //1 -left control ,2 - left shift, 4 left alt,5- ctrl+ alt (01 + 04) 8 - left gui, 16 - right control, 32 - right sift, 64 - right alt, 128 - right gui
	th[3] = 0x00;
	th[4] = 0x07; // the key code
	th[5] = 0x00;
	th[6] = 0x00;
	th[7] = 0x00;
	th[8] = 0x00;
	th[9] = 0x00;
	
	write(is, th, sizeof(th));
	
	/*for (i=0;i<1;i++){*/
		
		
	//th[4] = 0x0f;
	//write(is, th, sizeof(th));
	//th[4] = 0x2b;	
	//write(is, th, sizeof(th));
	//th[4] = 0x08;
	//write(is, th, sizeof(th));
	//th[4] = 0x1d;
	//write(is, th, sizeof(th));
	//th[4] = 0x111;
	//write(is, th, sizeof(th));
	
	/*}*/
		
	
	/*
	while(1){	
		bzero(cenas,1);
		cenas[0] = 30;
		write(is, th, 1);
		bzero(th2, 12);
		
		th2[0] = 0;
		write(cs,cenas,1);
		//write(cs,30,1);
	}*/
	
	/*
	while(1){
		
		// read data from the client
    	memset(buf, 0, sizeof(buf));
    	bytes_read = recv(csk, buf, sizeof(buf), 0);
    	if( bytes_read > 0 ) {
        	printf("received [%s]\n", buf);
    	}
		
		// read data from the client
    	memset(buf2, 0, sizeof(buf2));
    	bytes_read = recv(isk, buf2, sizeof(buf2), 0);
    	if( bytes_read > 0 ) {
        	printf("received [%s]\n", buf2);
    	}
		
	}
		*/
	
}
