
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

uint8_t cls[3];

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
	int opt, ctl, csk, isk,cs,is,i;
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


	while (1){

		memset(val,0, sizeof(val));

		if(scanf("%s", val)){
			
			if(!strcmp (val, "quit")){

				set_device_class(hdev, default_class);
				printf("Device class changed to: %s\n", default_class);
				close(cs);
				close(is);
				exit(1);
				
			}
			if(!strlen(val) > 2){
				char *val_x = strncat(&val[0], &val[1],1);
                                char *val_y = strncat(&val[2], &val[3],1);
				getchar();
				send_mouse_event(is, 0, atoi(val_x),atoi(val_y),0);
				

			}
			else{
				getchar();
				send_event(is, 0, atoi(val));
				//write(is, th, sizeof(th));
				//printf("%d\n", th[4]);
				//th[4] = 0x00;
				//write(is, th, sizeof(th));
				
			}
		}
	}
	
}
