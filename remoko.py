#
#      remoko.py
#
#      Copyright 2008 	Valerio Valerio <vdv100@gmail.com>
#						
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import dbus
import time
import os
import socket
import sys

input_connect = False

# Read record file
file_read = open('service_record.xml','r')
xml = file_read.read()

# Add service record to the BlueZ database
bus = dbus.SystemBus()
database = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'),
                                                        'org.bluez.Database')
handle = database.AddServiceRecordFromXML(xml)


# Check if input service is running, if yes terminate the service
bus_input = dbus.SystemBus()
input = dbus.Interface(bus_input.get_object('org.bluez', '/org/bluez/service_input'), 'org.bluez.Service')
input_status = input.IsRunning()

if input_status == True:
	input_connect = True
	cenas = input.Stop()
	
	print "--> BlueZ input service stopped"
	#os.system("dbus-send --system --print-reply --dest=org.bluez /org/bluez/service_input org.bluez.Service.Stop")

else:
	
	input_connect = False
	
#os.system("sudo ./hidclient")

sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6543))
	
reply = sock.recv(100)
print reply

bus_adapter = dbus.SystemBus()
adapter = dbus.Interface(bus_adapter.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')
input_status = adapter.ListConnections()
print input_status
print "You are connect to the address: " + str(input_status[-1])
client_name = adapter.GetRemoteName(input_status[-1])
print "connected to: " + str(client_name)


while 1:
	s = raw_input()
	sock.send(s)
	print sock.recv(100)
	if s == "quit":
		sock.close()
		sys.exit(1)

		database.RemoveServiceRecord(handle)

		# Restore initial input service condition
		if input_connect == True:
			input.Start()
			print "--> BlueZ input service started"
			#os.system("dbus-send --system --print-reply --dest=org.bluez /org/bluez/service_input org.bluez.Service.Start")
			


