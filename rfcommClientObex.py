import sys
import dbus

from bluetooth import *


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

service_matches = find_service(name = "OBEX Object Push", uuid = OBEX_OBJPUSH_CLASS)

if len(service_matches) == 0:
	print "couldnt find the service!"
	sys . exit(0)
	
first_match = service_matches[0]

port = first_match[ "port" ]
name = first_match[ "name" ]
host = first_match[ "host" ]

sock=BluetoothSocket( RFCOMM )
sock.connect( (host , port) )

paired = check_pairing(host)

if not paired:
	#put exception of authentication failed
	bus = dbus.SystemBus()

	obj = bus.get_object('org.bluez', '/org/bluez/hci0')
	adapter = dbus.Interface(obj, 'org.bluez.Adapter')

	print adapter.CreateBonding(host)

print "connecting to " , host



sock.send( "Hello!!" )

print 'port: ' + str(port)
print 'name: ' + str(name)
print 'host: ' + str(host)

data = sock.recv(80)
print "received: " , data
sock.close( )





