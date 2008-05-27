#L2cap- HID test server 


from bluetooth import *

server_sock= BluetoothSocket( L2CAP )

port = 0x1001

server_sock.bind(("",port))
server_sock.listen(1)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
advertise_service( server_sock, "VirtualKeyboardService",
                   service_id = uuid,
                   service_classes = [ uuid, HID_CLASS ],
                   profiles = [ HID_PROFILE ],
                   )
                   
client_sock,address = server_sock.accept()
print "Accepted connection from ",address

data = client_sock.recv(1024)
print "Data received:", data

while data:
    client_sock.send('Echo =>' + data)
    data = client_sock.recv(1024)
    print "Data received:",data

client_sock.close()
server_sock.close()
