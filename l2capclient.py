
import sys
import dbus
import bluetooth

def check_pairing(host):
	
	paired = False
	bus = dbus.SystemBus()
	
	obj = bus.get_object('org.bluez', '/org/bluez')
	manager = dbus.Interface(obj,'org.bluez.Manager')
	adapters = manager.ListAdapters()

	for adapter in adapters:
			obj2 = bus.get_object('org.bluez', adapter,)
			adapter = dbus.Interface(obj2, 'org.bluez.Adapter')
			if adapter.HasBonding(host):
				paired = True
                
	return paired       



sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
sock2=bluetooth.BluetoothSocket(bluetooth.L2CAP)

if len(sys.argv) < 2:
    print "usage: l2capclient.py < device addr>"
    sys.exit(2)

host=sys.argv[1]
#port should be available, make a l2cap scan

port = 17
port2 = 19

paired = check_pairing(host)

if not paired:
	#put exception of authentication failed
	bus = dbus.SystemBus()

	obj = bus.get_object('org.bluez', '/org/bluez/hci0')
	adapter = dbus.Interface(obj, 'org.bluez.Adapter')

	print adapter.CreateBonding(host)

print "connecting to " , host

print "trying to connect to %s on PSM 0x%X" % (host, port)

sock.connect((host, port))
sock2.connect((host, port2))

print "connected.  type stuff"
while True:
    data = raw_input()
    if(len(data) == 0): break
    sock.send(data)

sock.close()

