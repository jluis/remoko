import socket
import sys



sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6543))
while 1:
	s = raw_input()
	sock.send(s)
	print s
	print sock.recv(100)
sock.close()
