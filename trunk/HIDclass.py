import os


def setupHID(self):
	
	
	#Put exception here
	#Piscan enable page and inquiry scan.
	os.popen ("hciconfig hci0 piscan")
	os.popen ("hciconfig hci0 class 0x0005c0")
	
	# verify if sdpd is running
	
	print "Device class changed to keyboard/mouse combo"
	
def restoreBTDef(self):
	
	#Put exception
	#Pscan enable page scan, disable inquiry scan.
	os.popen ("hciconfig hci0 pscan")
	os.popen ("hciconfig hci0 class 0x120112")
	
	print "Device class changed to computer/handheld"
