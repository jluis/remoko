import sys
import dbus

from bluetooth import *


service_matches = find_service(name = "OBEX Object Push", uuid = OBEX_OBJPUSH_CLASS)

if len(service_matches) == 0:
	print "couldnt find the service!"
	sys . exit(0)
	
first_match = service_matches[0]

port = first_match[ "port" ]
name = first_match[ "name" ]
host = first_match[ "host" ]

print "connecting to " , host

sock=BluetoothSocket( RFCOMM )
sock.connect( (host , port) )
sock.send( "Hello!!" )

print 'port: ' + str(port)
print 'name: ' + str(name)
print 'host: ' + str(host)


bus = dbus.SystemBus()

obj = bus.get_object('org.bluez', '/org/bluez/hci0')
adapter = dbus.Interface(obj, 'org.bluez.Adapter')

print adapter.CreateBonding(host)


#manager = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'), 'org.bluez.Manager')
#adapters = manager.ListAdapters()
        
#for adapter in adapters:
	#adapter = dbus.Interface(bus.get_object('org.bluez', adapter), 'org.bluez.Adapter')
	## We asume that an adapter that can resolve the name is the "right" adapter
	#try:
		#name = adapter.GetRemoteName(host)
		
		#adapter.CreateBonding(host)
		#print 'Bonding returned'
		#if adapter.HasBonding(host):
			#print 'Bonding successfull'
		#else:
			#print 'Bonding failed'
		#break
	#except:
		#print 'Exception in BondingCreation (DBUS Methods)'
		#pass


data = sock.recv(80)
print "received: " , data
sock.close( )




