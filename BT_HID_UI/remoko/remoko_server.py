#
#      remoko_server.py
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
from threading import Thread


class Connect:
	
	def __init__(self):

		self.input_connect = False
		self.connect = False
		self.sock_open = False
		self.client_name = None
		self.client_addr = None
		self.error = False
		
		bus_input = dbus.SystemBus()
		self.input = dbus.Interface(bus_input.get_object('org.bluez', '/org/bluez/service_input'), 'org.bluez.Service')
		
		bus_adapter = dbus.SystemBus()
		self.adapter = dbus.Interface(bus_adapter.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')
		
		# Read record file
		#file_read = open('../data/service_record.xml','r')
		file_read = open('/usr/share/remoko/data/service_record.xml','r')
		xml = file_read.read()

		# Check if input service is running, if yes terminate the service

		try:

                       input_status = self.input.IsRunning()
		       print "passou"
                except:
		       print "ERROR: isRunning d-bus call not present"

		       try:
				os.system("/etc/init.d/bluetooth stop")
		       except:
				print "can't stop bluetooth services"
		       try:
				os.system("mv /usr/lib/bluetooth/plugins/libinput.so /usr/lib/bluetooth/plugins/libinput.so_back")
		       except:
				print "can't move input plugin"

		       try:
			
				os.system("/etc/init.d/bluetooth start")
		       except:
				print "can't start bluetooth services"

		       try:
				os.system("mv /usr/lib/bluetooth/plugins/libinput.so_back /usr/lib/bluetooth/plugins/libinput.so")
		       except:
				print "can't move input plugin"
			
				
				
                       input_status = False

                       self.input_connect = False

		#input_status = self.input.IsRunning()

		if input_status == True:
			
			try:
				cenas = self.input.Stop()
				self.input_connect = True
			except:

			       try:
					os.system("/etc/init.d/bluetooth stop")
		       	       except:
					print "can't stop bluetooth services"
			       try:
					os.system("mv /usr/lib/bluetooth/plugins/libinput.so /usr/lib/bluetooth/plugins/libinput.so_back")
			       except:
					print "can't move input plugin"

			       try:
			
					os.system("/etc/init.d/bluetooth start")
			       except:
					print "can't start bluetooth services"

			       try:
					os.system("mv /usr/lib/bluetooth/plugins/libinput.so_back /usr/lib/bluetooth/plugins/libinput.so")
			       except:
					print "can't move input plugin"
				
			       self.input_connect = False
			
			
			print "--> BlueZ input service stopped"
			#os.system("dbus-send --system --print-reply --dest=org.bluez /org/bluez/service_input org.bluez.Service.Stop")

		else:
			
			self.input_connect = False

		bus_input = dbus.SystemBus()
		self.input = dbus.Interface(bus_input.get_object('org.bluez', '/org/bluez/service_input'), 'org.bluez.Service')
		
		bus_adapter = dbus.SystemBus()
		self.adapter = dbus.Interface(bus_adapter.get_object('org.bluez', '/org/bluez/hci0'), 'org.bluez.Adapter')

		# Add service record to the BlueZ database
		bus = dbus.SystemBus()
		self.database = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'),
																'org.bluez.Database')
		self.handle = self.database.AddServiceRecordFromXML(xml)
	
			
	def start_connection(self):	
		
		self.deamon = start_deamon(self)
		self.deamon.start()
		self.listener = start_listener(self)
		self.listener.start()
		
	
	def send_mouse_event(self,btn,mov_x,mov_y, scroll):
		
		try:
			event = "02:" + str(btn) + ":" + str(mov_x) + ":" + str(mov_y) + ":" + str(scroll)
			self.sock.send(event)
		except:
			self.connect = False
			print "Disconnected"
		
	def send_keyboard_event(self,modifier,key):
		
		try:
			event = "01:" + str(modifier) + ":" + str(key) + ":"
			self.sock.send(event)
		except:
			self.connect = False
			print "Disconnected"
			
	def send_event(self, event):
		
		try:
			
			self.sock.send(event)
			
		except:
			self.connect = False
			print "disconnected"
			
	def terminate_connection(self):
		
		try:
			self.sock.send("quit")
		except:
			self.connect = False
			print "disconnected"

		self.database.RemoveServiceRecord(self.handle)

			# Restore initial input service condition
		if self.input_connect == True:
			self.input.Start()
			print "--> BlueZ input service started"
			
		print "Connection terminated"
			
				##os.system("dbus-send --system --print-reply --dest=org.bluez /org/bluez/service_input org.bluez.Service.Start")
				
class start_deamon(Thread):
	
	def __init__(self,remoko):
		
		Thread.__init__(self)
		self.remoko = remoko
		print "initializing daemon ..."
		
	def run(self):
		
		try:
			
			os.system("hidclient")
			
			
		except:
			
			print "Error in the daemon"



class start_listener(Thread):

	def __init__(self,remoko):
		
		Thread.__init__(self)
		self.remoko = remoko
		print "initializing listener ..."
		
	def run(self):


			while self.remoko.sock_open == False:

				try:
				
					self.remoko.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
					self.remoko.sock.connect(('localhost', 6543))
					self.remoko.sock_open = True
				
				except:
					print "waiting connection to remoko-server ..."
		
			#catch errors
			
			reply = self.remoko.sock.recv(100)
			if reply == "connected":
				print reply
				self.remoko.connect = True
			elif reply == "disconnected":
				self.remoko.connect = False
			try:	
						
				input_status = self.remoko.adapter.ListConnections()
				print input_status
				print "You are connect to the address: " + str(input_status[-1])
				client_name = self.remoko.adapter.GetRemoteName(input_status[-1])
				self.remoko.client_name = str(client_name)
				self.remoko.client_addr = str(input_status[-1])
				print "connected to: " + str(client_name)
			except:
				
				self.remoko.error = True
				print 'ERROR: Bluetooth is off'
			

