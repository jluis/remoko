import socket
import sys
import dbus


bus_adapter = dbus.SystemBus()
adapter = dbus.Interface(bus_adapter.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')
input_status = adapter.ListConnections()
print input_status
print "You are connect to the address: " + str(input_status[-1])
client_name = adapter.GetRemoteName(input_status[-1])
print "connected to: " + str(client_name)


sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6543))
while 1:
	s = raw_input()
	sock.send(s)
	print sock.recv(100)
	if s == "quit":
		sock.close()
		sys.exit(1)
