#!/usr/bin/env python
#
#      remoko.py
#
#      Copyright 2008 -2009 Valerio Valerio <vdv100@gmail.com>
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


import os
import sys
import time
import e_dbus
import evas
import evas.decorators
import edje
import edje.decorators
import ecore
import ecore.x
import ecore.evas
from dbus import SystemBus, Interface
from dbus.exceptions import DBusException
from optparse import OptionParser
from struct import unpack_from

from remoko_server import *
from remoko_key_mapper import *
from remoko_conf import *
from remoko_edje_group import *
from remoko_mouse import *
from remoko_disconnect import *
from remoko_connection_status import *
from remoko_about import *
from remoko_settings import *
from remoko_keyboard import *
from remoko_menu import *
from remoko_presentation import *
from remoko_multimedia import *
from remoko_accelerometer import *
from remoko_games import *

WIDTH = 480
HEIGHT = 640

TITLE = "remoko"
WM_NAME = "remoko"
WM_CLASS = "remoko"


#----------------------------------------------------------------------------#
def translate_key(self,keyname, keystring):
#----------------------------------------------------------------------------#
	if keyname == "Tab":
		return "Tab"
	elif keyname == "Return":
		return "Return"
	elif keyname == "Escape":
		return "Escape"
	elif keyname == "BackSpace":
		return "BackSpace"
	elif keyname == "Insert":
		return "Insert"
	elif keyname == "Home":
		return "Home"
	elif keyname == "Prior":
		return "Prior"
	elif keyname == "Delete":
		return "Delete"
	elif keyname == "End":
		return "End"
	elif keyname == "Next":
		return "Next"
	elif keyname == "Right":
		return "Right"
	elif keyname == "Left":
		return "Left"
	elif keyname == "Down":
		return "Down"
	elif keyname == "Up":
		return "Up"
	else:
		return keystring


#----------------------------------------------------------------------------#
class main(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "main")

	self.part_text_set("label_waiting", "Waiting for connection ... ")
	#ecore.timer_add(1.0,self.main.transition_to,"about")

	ecore.timer_add(1.0,self.check_connection)

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "quit":
		
		self.main.connection.terminate_connection()
		if self.main.connection.connect == False:
			os.system("pkill  -9 hidclient")
		self.main.on_exit()
		ecore.main_loop_quit()
		

    def check_connection(self):

		if self.main.connection_processed == True:

			if self.main.connection.connect == False:
				ecore.timer_add(1.0,self.check_connection)
				
			else:
			
				ecore.timer_add(1.0,self.check_client)
		else:
			ecore.timer_add(1.0,self.check_connection)

    def check_client(self):
		
		if self.main.connection.client_name == None:
			
			ecore.timer_add(1.0,self.check_client)
			
		else:
			
			self.part_text_set("label_waiting", "")
			self.part_text_set("label_connect_to", "Connected to: ")
			self.part_text_set("label_client", self.main.connection.client_name)
			ecore.idle_enterer_add( self.main.check_connection_status)
			ecore.timer_add(3.0,self.main.transition_to,"menu")

#----------------------------------------------------------------------------#
class bluetooth_off_alert(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "bluetooth_off_alert")
        
	self.part_text_set("label_error","Error: Bluetooth is off")
	self.part_text_set("label_connect", "Turn Bluetooth on ?")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):

	if source == "quit" or source == "no_option" :

		ecore.main_loop_quit()

	if source == "yes_option":

		self.main.power_on_bt()
		self.main.dbus_object.bluetooth_obj = True
		self.main.transition_to("main")
	



#----------------------------------------------------------------------------#
class conf_keys(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "conf_keys")
	self.shift = False
	self.ctrl = False
	self.alt = False
	self.press_f = False
	self.press_fpp = False
	self.press_w = False
	self.press_wi = False
	self.press_win = False
	self.hit = False
    
    def onShow( self ):
        self.focus = True
        self.main.window.x_window_virtual_keyboard_state_set(ecore.x.ECORE_X_VIRTUAL_KEYBOARD_STATE_ON)
        #if illume:
            #illume.kbd_show()

    def onHide( self ):
        self.focus = False
        self.main.window.x_window_virtual_keyboard_state_set(ecore.x.ECORE_X_VIRTUAL_KEYBOARD_STATE_OFF)
        #if illume:
            #illume.kbd_hide()

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		if self.main.current_conf_screen == "accelerometer_conf":
			prev = self.main.current_conf_screen
		else:
			prev = self.main.current_conf_screen + "_conf"

		prev_source = self.main.current_source + "_icon"
		local_key = str(self.main.current_source)
		
		if self.hit == False:
			
			self.hit = False
			self.main.transition_to(prev)
		
		elif len(self.main.key_text) > 6:
			#shift translation
			if self.main.key_text[0] == "s":
				text_value = self.main.key_mapper.mapper[self.main.key_text]
				self.main.groups[prev].part_text_set(prev_source,text_value + " ")
				self.main.save_local_conf(local_key,self.main.key_text)	
			else:
				self.main.groups[prev].part_text_set(prev_source,self.main.key_text + " ")
				self.main.save_local_conf(local_key,self.main.key_text)	
		elif self.main.key_text == "-":
			self.main.groups[prev].part_text_set(prev_source,"minus")
			self.main.save_local_conf(local_key,"minus")
		else:
			self.main.groups[prev].part_text_set(prev_source,self.main.key_text + " ")
			self.main.save_local_conf(local_key,self.main.key_text)
		self.hit = False
		self.main.transition_to(prev)

    @evas.decorators.key_down_callback
    def on_key_down( self, event ):
        key = event.string
	key_key = event.key
	key_value = event.keyname
	self.hit = True

	if key_value == "Shift_L":
		self.shift = True
			
	elif key_value == "Control_L":
		self.ctrl = True
			
	elif key_value == "Alt_L":
		self.alt = True

	elif key_value == "space":
		pass

	else:
	
		if self.shift == True:
			
			self.part_text_set("value","  "+ str(key)+ " ")
			self.shift = False
			self.main.key_text = "shift+"+str(key_value)
		
		elif self.alt == True and self.ctrl == True:

			self.part_text_set("value","ctrl+alt+" + str(key_key))
			self.ctrl = False
			self.alt = False
			self.main.key_text = "ctrl+alt+" + str(key_key)

		elif self.ctrl == True:

			self.part_text_set("value","ctrl+" + str(key_key))
			self.ctrl = False
			self.main.key_text = "ctrl+" + str(key_key)			

		elif self.alt == True:

			if key_value == "Tab":

				self.part_text_set("value","alt+" + str(key_value))	
				self.alt = False
				self.main.key_text = "alt+" + str(key_value)	
			else:
				

				self.main.key_text = translate_key(self,key_value,key)
				if self.main.key_text == "f":
					self.press_f = True
					self.part_text_set("value","alt+" + self.main.key_text)
				
				elif self.press_f == True:
					if self.main.key_text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
						if self.main.key_text == "1":
							self.press_fpp = True
						self.main.key_text = "alt+f" + self.main.key_text
						self.part_text_set("value",self.main.key_text)
						self.press_f = False
					
					else:
					
						self.press_f = False
						self.alt = False
						self.part_text_set("value","  " +self.main.key_text+ " ")
					
					
				elif self.press_fpp == True:
					if self.main.key_text in ("0", "1", "2"):
						self.main.key_text = "alt+f1" + self.main.key_text
						self.part_text_set("value",self.main.key_text)
						self.press_fpp = False
						self.alt = False
						
					else:
					
						self.press_fpp = False
						self.alt = False
						self.part_text_set("value","  " + self.main.key_text+" ")
					
				
				else:
					self.part_text_set("value","alt+" + str(key))	
					self.alt = False
					self.main.key_text = "alt+" + str(key)			

		else:
			self.main.key_text = translate_key(self,key_value,key)

			if self.main.key_text =="w":
				self.press_w = True
				self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_w == True:

				if self.main.key_text == "i":
					self.press_wi = True
					self.press_w = False
					self.part_text_set("value","w" + self.main.key_text+" ")
				else:
					
					self.press_w = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_wi == True:	

				if self.main.key_text == "n":
					self.press_win = True
					self.press_wi = False
					self.part_text_set("value","wi" + self.main.key_text+" ")
				else:
					
					self.press_w = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			elif self.press_win == True:

				self.press_win = False	
				self.part_text_set("value","win+" + self.main.key_text+" ")
				self.main.key_text = "win+" + self.main.key_text


			elif self.main.key_text == "f":
				self.press_f = True
				self.part_text_set("value","  " + self.main.key_text+" ")
				
			elif self.press_f == True:
				if self.main.key_text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
					if self.main.key_text == "1":
						self.press_fpp = True
					self.main.key_text = "f" + self.main.key_text
					self.part_text_set("value","  " + self.main.key_text+" ")
					self.press_f = False
					
				else:
					
					self.press_f = False
					self.part_text_set("value","  " + self.main.key_text+" ")
					
					
			elif self.press_fpp == True:
				if self.main.key_text in ("0", "1", "2"):
					self.main.key_text = "f1" + self.main.key_text
					self.part_text_set("value","  " + self.main.key_text+" ")
					self.press_fpp = False
						
				else:
					
					self.press_fpp = False
					self.part_text_set("value","  " + self.main.key_text+" ")

			
			else:
				self.part_text_set("value","  " + self.main.key_text+" ")
				
	

#----------------------------------------------------------------------------#
class GUI(object):
#----------------------------------------------------------------------------#
    def __init__( self, options, args ):
	
	self.remoko_conf = remoko_conf()
	self.load_local_confs()
	if self.fullscreen == "Yes":
		opt_fullscreen = True
	else:
		opt_fullscreen = False 
        edje.frametime_set(1.0 / options.fps)

        self.evas_canvas = EvasCanvas(
            fullscreen = opt_fullscreen,
            engine = options.engine,
            size = options.geometry
        )
	self.evas_canvas.main = self
	self.canvas = self.evas_canvas.evas_obj.evas
	self.window = self.evas_canvas.evas_obj
	self.connection_processed = False
	self.restore_conditions = False
	self.try_framework = 0
	self.key_text = ""
	self.gestures = False
	self.accelerometer_prev = "menu"
		
	self.key_mapper = key_mapper()
	

        self.groups = {}

        self.groups["swallow"] = edje_group(self, "swallow")
        self.evas_canvas.evas_obj.data["swallow"] = self.groups["swallow"]

        for page in ("main","mouse_ui", "menu", "disconnect", "connection_status", "keyboard_ui","about","bluetooth_off_alert","settings","accelerometer","accelerometer_conf","games","games_conf","multimedia","multimedia_conf","presentation","presentation_conf","conf_keys"):
		ctor = globals().get( page, None )
		if ctor:
			self.groups[page] = ctor( self )
			self.evas_canvas.evas_obj.data[page] = self.groups[page]


        self.groups["swallow"].show()

        self.groups["swallow"].part_swallow("area1", self.groups["main"])
        self.current_group = self.groups["main"]
        self.previous_group = self.groups["menu"]
        self.in_transition = False
	self.current_conf_screen = None
	self.current_source = None
	self.dbus_accel()
	self.dbus_objectInit()
	self.initialize_remoko_server()

    def check_connection_status(self):
	if self.connection.connect == False:
		self.transition_to("disconnect")
		print "->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DISC"

	else:
		ecore.timer_add( 10.0, self.check_connection_status)
	
	
    def check_bt_status(self):
		
	file = open("/sys/bus/platform/devices/neo1973-pm-bt.0/power_on")
	status = file.readline()
	if status.find('0') > -1:
		print "off"
		return "off"
	else:
		print "on"
		return "on"
		
	file.close()

    def power_on_bt(self):
	
	self.restore_conditions = True
	os.system("echo 1 > /sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/power_on")
	os.system("echo 0 > /sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/reset")
	
    def dbus_objectInit( self ):
        print "dbus_objectInit..."
        global dbus_object
	if self.try_framework == 2:
		status = self.check_bt_status()
		if status == "off":
			self.transition_to("bluetooth_off_alert")
		else:
			self.dbus_object.bluetooth_obj = True
		print 'You are using ASU'
		return False
        if dbus_object is None:
            self.dbus_object = DBusObject(self)
        if not self.dbus_object.initialize():
            # try again later
            ecore.timer_add( 1.0, self.dbus_objectInit )
	    self.try_framework += 1 
            return False

    def dbus_accel( self ):
       print "dbus_objectInit..."
       global dbus_object
	
       if dbus_object is None:
           self.dbus_object = DBusObject(self)
       if not self.dbus_object.initialize_accel():
           print "accel error"
           return False
        
	
    def on_exit(self):
	
	if self.restore_conditions == True:

		os.system("echo 1 > /sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/reset")
	
        

    def initialize_remoko_server(self, addr=1):

	if self.dbus_object.bluetooth_obj == True:

		self.connection = Connect()
		self.connection.start_connection(addr)
		self.connection_processed = True
        else:
		ecore.timer_add(1.0,self.initialize_remoko_server)
	
    def load_local_confs(self):
	#settings
	self.fullscreen = self.remoko_conf.fullscreen
	self.scroll = int(self.remoko_conf.scroll)
	self.accelerometer = self.remoko_conf.accelerometer
	#presentation
	self.previous_key = self.remoko_conf.previous_key
	self.next_key = self.remoko_conf.next_key
	self.fullscreen_key = self.remoko_conf.fullscreen_key
	self.no_fullscreen_key = self.remoko_conf.no_fullscreen_key
	#multimedia profile
	self.play_key = self.remoko_conf.play_key
	self.pause_key = self.remoko_conf.pause_key
	self.stop_key = self.remoko_conf.stop_key
	self.forward_key = self.remoko_conf.forward_key
	self.backward_key = self.remoko_conf.backward_key
	self.volume_m_key = self.remoko_conf.volume_m_key
	self.volume_p_key = self.remoko_conf.volume_p_key
	self.fullscreen_key_m = self.remoko_conf.fullscreen_key_m
	self.no_fullscreen_key_m = self.remoko_conf.no_fullscreen_key_m
	#accelerometer profile
	self.up_key = self.remoko_conf.up_key
	self.up_down_key = self.remoko_conf.up_down_key
	self.right_key = self.remoko_conf.right_key
	self.right_left_key = self.remoko_conf.right_left_key
	self.left_key = self.remoko_conf.left_key
	self.left_right_key = self.remoko_conf.left_right_key
	self.down_key = self.remoko_conf.down_key
	self.down_up_key = self.remoko_conf.down_up_key
	self.forw_backw_key = self.remoko_conf.forw_backw_key
	self.shake_shake_key = self.remoko_conf.shake_shake_key
	self.z_key = self.remoko_conf.z_key
	self.horizontal_circle_key = self.remoko_conf.horizontal_circle_key
	#games profile
	self.up_key = self.remoko_conf.up_key
	self.down_key = self.remoko_conf.down_key
	self.right_key = self.remoko_conf.right_key
	self.left_key = self.remoko_conf.left_key
	self.a_key = self.remoko_conf.a_key
	self.b_key = self.remoko_conf.b_key
	self.c_key = self.remoko_conf.c_key
	self.d_key = self.remoko_conf.d_key
	

    def save_local_conf(self, button_name, key):
	
	if button_name == "previous_key":

		self.previous_key = key
		self.remoko_conf.set_option("presentation","previous_key",key)

	elif button_name == "next_key":

		self.next_key = key
		self.remoko_conf.set_option("presentation","next_key",key)

	elif button_name == "fullscreen_key":

		self.fullscreen_key = key
		self.remoko_conf.set_option("presentation","fullscreen_key",key)

	elif button_name == "no_fullscreen_key":

		self.no_fullscreen_key = key
		self.remoko_conf.set_option("presentation","no_fullscreen_key",key)

	elif button_name == "play_key":

		self.play_key = key
		self.remoko_conf.set_option("multimedia","play_key",key)

	elif button_name == "pause_key":

		self.pause_key = key
		self.remoko_conf.set_option("multimedia","pause_key",key)

	elif button_name == "stop_key":

		self.stop_key = key
		self.remoko_conf.set_option("multimedia","stop_key",key)

	elif button_name == "forward_key":

		self.forward_key = key
		self.remoko_conf.set_option("multimedia","forward_key",key)

	elif button_name == "backward_key":

		self.backward_key = key
		self.remoko_conf.set_option("multimedia","backward_key",key)

	elif button_name == "volume_p_key":

		self.volume_p_key = key
		self.remoko_conf.set_option("multimedia","volume_p_key",key)

	elif button_name == "volume_m_key":

		self.volume_m_key = key
		self.remoko_conf.set_option("multimedia","volume_m_key",key)
	
	
	elif button_name == "fullscreen_key_m":

		self.fullscreen_key_m = key
		self.remoko_conf.set_option("multimedia","fullscreen_key_m",key)

	elif button_name == "no_fullscreen_key_m":

		self.no_fullscreen_key_m = key
		self.remoko_conf.set_option("multimedia","no_fullscreen_key_m",key)

	elif button_name == "up_key":

		self.up_key = key
		self.remoko_conf.set_option("accelerometer","up_key",key)

	elif button_name == "up_down_key":

		self.up_down_key = key
		self.remoko_conf.set_option("accelerometer","up_down_key",key)

	elif button_name == "right_key":

		self.right_key = key
		self.remoko_conf.set_option("accelerometer","right_key",key)

	elif button_name == "right_left_key":

		self.right_left_key = key
		self.remoko_conf.set_option("accelerometer","right_left_key",key)
	
	elif button_name == "left_key":

		self.left_key = key
		self.remoko_conf.set_option("accelerometer","left_key",key)

	elif button_name == "left_right_key":

		self.left_right_key = key
		self.remoko_conf.set_option("accelerometer","left_right_key",key)
	
	elif button_name == "down_key":

		self.down_key = key
		self.remoko_conf.set_option("accelerometer","down_key",key)

	elif button_name == "down_up_key":

		self.down_up_key = key
		self.remoko_conf.set_option("accelerometer","down_up_key",key)

	elif button_name == "forw_backw_key":

		self.forw_backw_key = key
		self.remoko_conf.set_option("accelerometer","forw_backw_key",key)

	elif button_name == "shake_shake_key":

		self.shake_shake_key = key
		self.remoko_conf.set_option("accelerometer","shake_shake_key",key)
	
	elif button_name == "z_key":

		self.z_key = key
		self.remoko_conf.set_option("accelerometer","z_key",key)

	elif button_name == "horizontal_circle_key":

		self.horizontal_circle_key = key
		self.remoko_conf.set_option("accelerometer","horizontal_circle_key",key)

	elif button_name == "up_key":

		self.up_key = key
		self.remoko_conf.set_option("games","up_key",key)

	elif button_name == "down_key":

		self.down_key = key
		self.remoko_conf.set_option("games","down_key",key)

	elif button_name == "right_key":

		self.right_key = key
		self.remoko_conf.set_option("games","right_key",key)

	elif button_name == "left_key":

		self.left_key = key
		self.remoko_conf.set_option("games","left_key",key)
	
	elif button_name == "a_key":

		self.a_key = key
		self.remoko_conf.set_option("games","a_key",key)

	elif button_name == "b_key":

		self.b_key = key
		self.remoko_conf.set_option("games","b_key",key)
	
	elif button_name == "c_key":

		self.c_key = key
		self.remoko_conf.set_option("games","c_key",key)

	elif button_name == "d_key":

		self.d_key = key
		self.remoko_conf.set_option("games","d_key",key)

    def run( self ):
        ecore.main_loop_begin()
	
    def shutdown( self ):
        ecore.main_loop_quit()

    def transition_to(self, target):
        if self.current_group == self.groups[target]:
            return
        print "transition to", target
        self.in_transition = True

        self.previous_group = self.current_group

        self.current_group = self.groups[target]
        self.current_group.onShow()
        self.current_group.signal_emit("visible", "")
        self.groups["swallow"].part_swallow("area1", self.current_group)
        self.previous_group.signal_emit("fadeout", "")

    def transition_finished(self):
        print "finished"
        self.previous_group.onHide()
        self.previous_group.hide()
        self.groups["swallow"].part_swallow("area1", self.current_group)
        self.in_transition = False
        
       

	
#----------------------------------------------------------------------------#
class DBusObject( object ):
#----------------------------------------------------------------------------#

    def __init__( self,main ):
        self.objects = {}
        self.onResourceChanged = []
        self.onCallStatus = []
        self.onNetworkStatus = []
        self.onIdleStateChanged = []
        self.ignoreSuspend = False

        self.framework_obj = None
        self.gsm_device_obj = None
        self.gsm_device_iface = None
        self.usage_iface = None
        self.device_iface = None
        self.device_power_iface = None
        self.idlenotifier_obj = None
        self.idlenotifier_iface = None
        self.inputnotifier_obj = None
        self.inputnotifier_iface = None
        self.display_obj = None
        self.display_iface = None

        self.fullinit = False
	self.bluetooth_obj = False
	self.main = main

    def tryGetProxy( self, busname, objname ):
        object = None
        try:
            object = self.objects[ "%s:%s" % ( busname, objname ) ]
        except KeyError:
            try:
                object = self.bus.get_object( busname, objname )
            except DBusException, e:
                print "could not create proxy for %s:%s" % ( busname, objname ), e
            else:
                self.objects[ "%s:%s" % ( busname, objname ) ] = object
        return object

    def initialize( self ):
        if self.fullinit:
            return True
        try:
            self.bus = SystemBus( mainloop=e_dbus.DBusEcoreMainLoop() )
        except DBusException, e:
            print "could not connect to dbus_object system bus:", e
            return False

	failcount = 0

        # request bluetooth services
        self.usage_obj = self.tryGetProxy( 'org.freesmartphone.ousaged', '/org/freesmartphone/Usage' )
        if ( self.usage_obj is not None ) and ( self.usage_iface is None ):
            self.usage_iface = Interface(self.usage_obj, 'org.freesmartphone.Usage')
            self.usage_iface.connect_to_signal( "ResourceChanged", self.cbResourceChanged )
            self.usage_iface.RequestResource("Bluetooth")
        if self.usage_obj is None:
            failcount += 1

        else:
	    self.bluetooth_obj = True
            print "usage ok", self.usage_iface
        
        print "failcount=", failcount
        if failcount == 0:
            self.fullinit = True
        return self.fullinit	

    def initialize_accel( self ):
        if self.fullinit:
            return True
        try:
            self.bus = SystemBus( mainloop=e_dbus.DBusEcoreMainLoop() )
        except DBusException, e:
            print "could not connect to dbus_object system bus:", e
            return False

	failcount = 0

	#accel
	self.accel_obj = self.tryGetProxy( 'org.openmoko.accelges', '/org/openmoko/accelges/Recognizer' )
	if self.accel_obj is None:
		print "error in proxy"
	else:
		print "proxy ok"
		try:
			self.accel_iface = Interface(self.accel_obj, 'org.openmoko.accelges.Recognizer')
    			self.accel_iface.connect_to_signal( "Recognized", self.cbReconizedGest )
			print "interface ok"
			self.main.gestures = True
			
		except  DBusException, e:
	    		print "error in interface"
        
        print "failcount=", failcount
        if failcount == 0:
            self.fullinit = True
        return self.fullinit	


    #def cbResourceChanged( self, resourcename ):
     #   for cb in self.onResourceChanged:
      #      cb( resourcename=resourcename )

    def cbResourceChanged( self, resourcename, state, attributes ):
        for cb in self.onResourceChanged:
            cb( resourcename=resourcename, state=state, attributes=attributes )

    def cbReconizedGest(self,id):
		if self.main.accelerometer == "No":
			pass
		else:
			
			if id == "right, and return":

				key = self.main.right_left_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id =="horizontal circle":

				key = self.main.horizontal_circle_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)
				
			elif id =="forward, backward":

				key = self.main.forw_backw_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)
				
			elif id =="shake, shake":

				key = self.main.shake_shake_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id =="left, and return":

				key = self.main.left_right_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id == "up, and return":

				key = self.main.up_down_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id =="down":

				key = self.main.down_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id == "up":

				key = self.main.up_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id =="down, and return":
				
				key = self.main.down_up_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)
			
			elif id == "right":
				
				key = self.main.right_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id == "left":

				key = self.main.left_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)

			elif id == "z":

				key = self.main.z_key
				modif, val = key_dec(self,key)
				value = self.main.key_mapper.mapper[str(val)]
				self.main.connection.send_keyboard_event(modif,value)
				
			else:
				pass
		
		

    
#----------------------------------------------------------------------------#
class EvasCanvas(object):
#----------------------------------------------------------------------------#
    def __init__(self, fullscreen, engine, size):
        if engine == "x11":
            f = ecore.evas.SoftwareX11
        elif engine == "x11-16":
            if ecore.evas.engine_type_supported_get("software_16_x11"):
                f = ecore.evas.SoftwareX11_16
            else:
                print "warning: x11-16 is not supported, fallback to x11"
                f = ecore.evas.SoftwareX11

        self.evas_obj = f(w=size[0], h=size[1])
        self.evas_obj.callback_delete_request = self.on_delete_request
        self.evas_obj.callback_resize = self.on_resize

        self.evas_obj.title = TITLE
        self.evas_obj.name_class = (WM_NAME, WM_CLASS)
        self.evas_obj.fullscreen = fullscreen
        self.evas_obj.size = size
        self.evas_obj.evas.image_cache_set( 6*1024*1024 )
        self.evas_obj.evas.font_cache_set( 2*1024*1024 )
        self.evas_obj.show()

    def on_resize(self, evas_obj):
        x, y, w, h = evas_obj.evas.viewport
        size = (w, h)
        evas_obj.data["swallow"].size = size

    def on_delete_request(self, evas_obj):

	self.main.connection.terminate_connection()

	if self.main.connection.connect == False:
		os.system("pkill  -9 hidclient")
	self.main.on_exit()
	ecore.main_loop_quit()
#----------------------------------------------------------------------------#
class MyOptionParser(OptionParser):
#----------------------------------------------------------------------------#
    def __init__(self):
        OptionParser.__init__(self)
        self.set_defaults(fullscreen = False)
        self.add_option("-e",
                      "--engine",
                      type="choice",
                      choices=("x11", "x11-16"),
                      default="x11-16",
                      help=("which display engine to use (x11, x11-16), "
                            "default=%default"))
        self.add_option("--fullscreen",
                      action="store_true",
                      dest="fullscreen",
                      help="launch in fullscreen")
        self.add_option("--no-fullscreen",
                      action="store_false",
                      dest="fullscreen",
                      help="launch in a window")
        self.add_option("-g",
                      "--geometry",
                      type="string",
                      metavar="WxH",
                      action="callback",
                      callback=self.parse_geometry,
                      default=(WIDTH, HEIGHT),
                      help="use given window geometry")
        self.add_option("-f",
                      "--fps",
                      type="int",
                      default=20,
                      help="frames per second to use, default=%default")
        self.add_option("-s",
                      "--start",
                      type="string",
                      default=None,
                      help="start with the given page")

    def parse_geometry(option, opt, value, parser):
        try:
            w, h = value.split("x")
            w = int(w)
            h = int(h)
        except Exception, e:
            raise optparse.OptionValueError("Invalid format for %s" % option)
        parser.values.geometry = (w, h)


if __name__ == "__main__":

    options, args = MyOptionParser().parse_args()
    dbus_object = None
    gui = GUI( options, args )
    try:
        gui.run()
    except KeyboardInterrupt:
        gui.shutdown()
        del gui




