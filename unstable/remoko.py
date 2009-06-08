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

WIDTH = 480
HEIGHT = 640

TITLE = "remoko"
WM_NAME = "remoko"
WM_CLASS = "remoko"


edjepaths = "remoko.edj themes/remoko.edj /usr/share/remoko/themes/remoko.edj".split()

for i in edjepaths:
    if os.path.exists( i ):
       global edjepath
       edjepath = i
       break
else:
    raise Exception( "remoko.edj not found. looked in %s" % edjepaths )


#-------------------------------------------------------------------------#
def mouse_position(self,x1,y1):
#-------------------------------------------------------------------------#	
	x = x1 - self.x_init
	y = y1 - self.y_init
	
	self.x_init = x1
	self.y_init = y1
			
	return x,y
#-------------------------------------------------------------------------#
def key_dec(self,key):
#-------------------------------------------------------------------------#
	self.shift = False
	self.ctrl = False
	self.alt = False
	self.win = False
	self.modif = ""
	self.val = ""
	if len(key) < 5:

		return "00", key

	else:

		key_split = key.split("+")
		
		for i in key_split:
			
			if i == "shift":
				self.shift = True
			
			elif i == "ctrl":
				self.ctrl = True
			
			elif i == "alt":
				self.alt = True
			elif i == "win":
				self.win = True
			
			else:
			
				if self.shift == True:

					self.modif = "02"
					self.shift = False
					self.val = str(i)

				if self.win == True:

					self.modif = "08"
					self.win = False
					self.val = str(i)

				elif self.ctrl == True and self.alt == True:

					self.ctrl = False
					self.alt = False
					self.modif = "05"
					self.val = str(i)
				
				elif self.ctrl == True:

					
					self.ctrl = False
					self.modif = "01"
					self.val = str(i)
				
				elif self.alt == True:
					
					self.alt = False
					self.modif = "04"
					self.val = str(i)
			
				else:	
					self.modif = "00"
					self.val = str(i)
	
	return self.modif,self.val
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
class edje_group(edje.Edje):
#----------------------------------------------------------------------------#
    def __init__(self, main, group, parent_name="main"):
        self.main = main
        self.parent_name = parent_name
        global edjepath
        f = edjepath
        try:
            edje.Edje.__init__(self, self.main.evas_canvas.evas_obj.evas, file=f, group=group)
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (f, e))
        self.size = self.main.evas_canvas.evas_obj.evas.size

    def onShow( self ):
        pass

    def onHide( self ):
        pass

    @edje.decorators.signal_callback("mouse,clicked,1", "button_bottom_right")
    def on_edje_signal_button_bottom_right_pressed(self, emission, source):
        self.main.transition_to(self.parent_name)

    @edje.decorators.signal_callback("finished_transition", "*")
    def on_edje_signal_finished_transition(self, emission, source):
        self.main.transition_finished()

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
class disconnect(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "disconnect")
        
	self.part_text_set("label_error","Error: Disconnected by remote device")
	self.part_text_set("label_connect", "Open connection again ?")
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "quit" or source == "no_option" :
		
		self.main.connection.terminate_connection()
		if self.main.connection.connect == False:
			os.system("pkill  -9 hidclient")
		self.main.on_exit()
		ecore.main_loop_quit()

	if source == "yes_option":

		self.main.connection.terminate_connection()
		if self.main.connection.connect == False:
			os.system("pkill  -9 hidclient")
		self.main.initialize_remoko_server()
		self.main.groups["main"].part_text_set("label_connect_to", "")
		self.main.groups["main"].part_text_set("label_client", "")
		self.main.groups["main"].part_text_set("label_waiting", "Waiting for connection ... ")
		ecore.timer_add(1.0,self.main.groups["main"].check_client)
		self.main.transition_to("main")
		
#----------------------------------------------------------------------------#
class connection_status(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "connection_status")

        
    	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

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
class about(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "about")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

#----------------------------------------------------------------------------#
class settings(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "settings")
        self.part_text_set("fullscreen_option",str(self.main.remoko_conf.fullscreen))
	self.part_text_set("scroll_option", str(self.main.remoko_conf.scroll))
	self.part_text_set("accelerometer_option",self.main.accelerometer)
	self.scroll_value = int(self.main.remoko_conf.scroll)
	self.fscreen_option = str(self.main.remoko_conf.fullscreen)
	self.accelerometer_option = self.main.accelerometer

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	 

	if source == "back":
		
		self.main.remoko_conf.set_option("user","fullscreen",self.fscreen_option)
		self.main.remoko_conf.set_option("user","scroll",self.scroll_value)
		self.main.remoko_conf.save_options()
		self.main.scroll = self.scroll_value
		self.main.transition_to("menu")

	elif source == "fullscreen_option":
		
		if self.fscreen_option == "Yes":
			
			self.part_text_set("fullscreen_option","No")
			self.fscreen_option = "No"
			self.main.window.fullscreen = False

		elif self.fscreen_option == "No":
			
			self.part_text_set("fullscreen_option","Yes")
			self.fscreen_option = "Yes"
			self.main.window.fullscreen = True

	elif source == "scroll_right_icon":
		
		if self.scroll_value < 9:
			self.scroll_value += 1
			self.part_text_set("scroll_option", str(self.scroll_value))
	
	elif source == "scroll_left_icon":
		
		if self.scroll_value >= 1:
			self.scroll_value -= 1
			self.part_text_set("scroll_option", str(self.scroll_value))

	elif source == "accelerometer_option":
		
		if self.accelerometer_option == "Yes":
			
			self.part_text_set("accelerometer_option","No")
			self.accelerometer_option = "No"
			self.main.accelerometer = "No"
			

		elif self.fscreen_option == "No":
			
			self.part_text_set("accelerometer_option","Yes")
			self.accelerometer_option = "Yes"
			self.main.accelerometer = "Yes"

#----------------------------------------------------------------------------#
class menu(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "menu")
	self.part_text_set( "label_title", "ReMoko" )
        
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
 
		if source == "quit":
		
			self.main.connection.terminate_connection()

			if self.main.connection.connect == False:
				os.system("pkill -9 hidclient")
			self.main.on_exit()
			ecore.main_loop_quit()
			
		elif source == "mouse":
			
			self.main.transition_to("mouse_ui")

		elif source == "keyboard":
			
			self.main.transition_to("keyboard_ui")

		elif source == "presentation":
			
			self.main.transition_to("presentation")

		elif source == "multimedia":
			
			self.main.transition_to("multimedia")

		elif source == "games":
			
			self.main.transition_to("games")

		elif source == "accelerometer":
			self.main.accelerometer_prev = "menu"
			self.main.transition_to("accelerometer")

		elif source == "connection":

			if self.main.connection.connect == True:
				self.main.groups["connection_status"].part_text_set("label_connect_to","Connected to:")
    				self.main.groups["connection_status"].part_text_set("label_client", self.main.connection.client_name)
				self.main.groups["connection_status"].part_text_set("label_addr",self.main.connection.client_addr)
			else:
				self.part_text_set("label_not_connect","You are not connect to any device")
		
			self.main.transition_to("connection_status")

		elif source == "about":
			
			self.main.groups["about"].part_text_set("label_version","ReMoko v0.3")
			self.main.groups["about"].part_text_set("label_developed","Developed by:")
			self.main.groups["about"].part_text_set("label_name","Valerio Valerio")
			self.main.groups["about"].part_text_set("label_email","<vdv100@gmail.com>")
			self.main.groups["about"].part_text_set("label_thanks","Thanks to:")
			self.main.groups["about"].part_text_set("label_claudio","Claudio Takahasi")
			self.main.groups["about"].part_text_set("label_daniel","Daniel Willmann ")
			self.main.groups["about"].part_text_set("label_joachim","Joachim Breitner")
			
			
			self.main.transition_to("about")	

		elif source == "conf":

			self.main.transition_to("settings")			
		else:
			
			print "feature not implemented yet :) "

#----------------------------------------------------------------------------#
class mouse_ui(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "mouse_ui")
        self.x_init, self.y_init = 0,0
        self.mouse_down = False
        self.first_touch = True
        self.button_hold = False
	self.scroll_pos = 0
	self.tape_mouse_area = 0
	

    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_mouse_down(self, emission, source):
		
		self.mouse_down = True
		self.tape_mouse_area = time.time()

    		

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_mouse_up(self, emission, source):

		if source == "mouse_area":
			tape_time = time.time() - self.tape_mouse_area
			
			if tape_time < 0.2:

				self.main.connection.send_mouse_event(1,0,0,0)
				self.main.connection.send_event("btn_up")

		self.mouse_down = False
		self.first_touch = True
		self.x_init, self.y_init = 0,0
		

    @edje.decorators.signal_callback("mouse_over_scroll", "*") 
    def on_mouse_over_scroll(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:

				tmp,self.scroll_pos = self.main.canvas.pointer_canvas_xy			
				self.first_touch = False
			else:

				tmp,y_scroll = self.main.canvas.pointer_canvas_xy	

				if y_scroll > self.scroll_pos + self.main.scroll:

					self.scroll_pos = y_scroll
					self.main.connection.send_event("02:00:000:000:255")
					
					

				elif y_scroll < self.scroll_pos - self.main.scroll:

					self.scroll_pos = y_scroll
					self.main.connection.send_event("02:00:000:000:01")
					
					
				else:

					pass

		else:

			print "mouse_over_scroll"

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_over_area(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:
				
				self.first_touch = False
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)
				
				
				if self.button_hold == True:
					
					mov = "02:01:" + str(x1) + ":" + str(y1) + ":000"
					
					self.main.connection.send_mouse_event(01,x1,y1,00)
					
				else:	
					
					mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
					
					self.main.connection.send_mouse_event(00,x1,y1,00)

		else:
			pass	
			
   
	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_mouse_click(self, emission, source):
    	
		
		if source == "bt_right":
			
			self.main.connection.send_mouse_event(2,0,0,0)
			self.main.connection.send_event("btn_up")
			
		elif source == "bt_left":
			
			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_event("btn_up")
			
		elif source == "bt_hold":
			
			if self.button_hold == True:
				
				self.button_hold = False
				
				self.signal_emit("hold_released", "")
				self.main.connection.send_event("btn_up")

				
			else:
				
				self.button_hold = True
				self.signal_emit("hold_pressed", "")
				
		elif source == "bt_middle":
			
			self.main.connection.send_mouse_event(4,0,0,0)
			self.main.connection.send_event("btn_up")

			
			
		elif source == "back":
	
			print self.main.previous_group
			self.main.transition_to("menu")
				
		else:
				
			pass

#----------------------------------------------------------------------------#
class keyboard_ui(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "keyboard_ui")
        self.shift = False
        self.alt = False
        self.ctrl = False
	self.tape_mouse_area = 0
	self.x_init, self.y_init = 0,0
        self.mouse_down = False
        self.first_touch = True

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

    @evas.decorators.key_down_callback
    def on_key_down( self, event ):
    	print event
        key = event.keyname
	
	try:
		if key == "Shift_L":
			self.shift = True
			
		elif key == "Control_L":
			self.ctrl = True
			
		elif key == "Alt_L":
			self.alt = True
			
		else:
			
			value = self.main.key_mapper.mapper[str(key)]
			
			if self.shift == True:
				self.main.connection.send_keyboard_event("02",value)
				self.shift = False
			
			elif self.alt == True and self.ctrl == True:
				self.main.connection.send_keyboard_event("05",value)
				self.ctrl = False
				self.alt = False
				
			elif self.ctrl == True:
				self.main.connection.send_keyboard_event("01",value)
				self.ctrl = False
				
			elif self.alt == True:
				self.main.connection.send_keyboard_event("04",value) 	
				self.alt = False
			
			else:
				self.main.connection.send_keyboard_event("00",value)
	except:
		print "Key error --->>>"

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

######## Mouse Area ##############################

    @edje.decorators.signal_callback("mouse,down,1", "background")
    def on_mouse_down(self, emission, source):
		
		self.mouse_down = True
		self.tape_mouse_area = time.time()

    @edje.decorators.signal_callback("mouse,up,1", "background")
    def on_mouse_up(self, emission, source):

		
		tape_time = time.time() - self.tape_mouse_area
		
		if tape_time < 0.2:

			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_event("btn_up")

		self.mouse_down = False
		self.first_touch = True
		self.x_init, self.y_init = 0,0

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_over_area(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:
				
				self.first_touch = False
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)
					
				mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
				self.main.connection.send_mouse_event(00,x1,y1,00)

		else:
			pass	


#----------------------------------------------------------------------------#
class presentation(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "presentation")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source ==	"conf_keys":
		
		self.main.transition_to("presentation_conf")
	
	elif source == "conf_gestures":

		self.main.accelerometer_prev = "presentation"
		self.main.transition_to("accelerometer_conf")

	elif source == "previous":


		key = self.main.previous_key
		modif, val = key_dec(self,key)
		
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "next":

		key = self.main.next_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "fullscreen":

		key = self.main.fullscreen_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "no_fullscreen":

		key = self.main.no_fullscreen_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

#----------------------------------------------------------------------------#
class presentation_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "presentation_conf")
	count = 0
	self.prev_key = ""
	self.next_key = ""
	self.full_key = ""
	self.no_full_key = ""
	for i in (self.main.previous_key,self.main.next_key,self.main.fullscreen_key, self.main.no_fullscreen_key):
		if len(i) > 6:
			#shift translation
			if i[0] == "s":
				text_value = self.main.key_mapper.mapper[i]
				count +=1
		else:
			text_value = i
			count +=1
		if count == 1:
			self.prev_key = text_value
		elif count == 2:
			self.next_key = text_value
		elif count == 3:
			self.full_key = text_value
		elif count == 4:
			self.no_full_key = text_value
				
		 
	self.part_text_set("previous_key_icon", self.prev_key)
	self.part_text_set("next_key_icon", self.next_key)
	self.part_text_set("fullscreen_key_icon", self.full_key)
	self.part_text_set("no_fullscreen_key_icon", self.no_full_key)
	self.key_value = ""

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		self.main.remoko_conf.save_options()
		self.main.transition_to("presentation")	
	else:
		if source == "previous_key":

			self.key_value = self.part_text_get("previous_key_icon")
			self.main.key_text = self.key_value

		elif source == "next_key":

			self.key_value = self.part_text_get("next_key_icon")
			self.main.key_text = self.key_value

		elif source == "fullscreen_key":

			self.key_value = self.part_text_get("fullscreen_key_icon")
			self.main.key_text = self.key_value

		elif source == "no_fullscreen_key":

			self.key_value = self.part_text_get("no_fullscreen_key_icon")
			self.main.key_text = self.key_value

		self.main.current_conf_screen = "presentation"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value"," "+self.key_value+ " ")
		self.main.transition_to("conf_keys")	
	

#----------------------------------------------------------------------------#
class multimedia(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "multimedia")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")	
		
	elif source ==	"conf_keys":
		
		self.main.transition_to("multimedia_conf")

	elif source == "conf_gestures":

		self.main.accelerometer_prev = "multimedia"
		self.main.transition_to("accelerometer_conf")

	elif source == "play":

		key = self.main.play_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "pause":

		key = self.main.pause_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "stop":

		key = self.main.stop_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "forward":

		key = self.main.forward_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "backward":

		key = self.main.backward_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "volume-":

		key = self.main.volume_m_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "volume+":

		key = self.main.volume_p_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "fullscreen":

		key = self.main.fullscreen_key_m
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "no_fullscreen":

		key = self.main.no_fullscreen_key_m
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)


#----------------------------------------------------------------------------#
class multimedia_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "multimedia_conf")
	count = 0
	self.play_key = ""
	self.pause_key = ""
	self.stop_key = ""
	self.forw_key = ""
	self.backw_key = ""
	self.vol_m_key = ""
	self.vol_p_key = ""
	self.full_key = ""
	self.no_full_key = ""

	for i in (self.main.play_key,self.main.pause_key,self.main.stop_key,self.main.forward_key,self.main.backward_key, self.main.volume_m_key,self.main.volume_p_key,self.main.fullscreen_key_m, self.main.no_fullscreen_key_m):
		if len(i) > 6:
			#shift translation
			if i[0] == "s":
				text_value = self.main.key_mapper.mapper[i]
				count +=1
		else:
			text_value = i
			count +=1
		if count == 1:
			self.play_key = text_value
		elif count == 2:
			self.pause_key = text_value
		elif count == 3:
			self.stop_key = text_value
		elif count == 4:
			self.forw_key = text_value
		elif count == 5:
			self.backw_key = text_value
		elif count == 6:
			self.vol_m_key = text_value
		elif count == 7:
			self.vol_p_key = text_value
		elif count == 8:
			self.full_key = text_value
		elif count == 9:
			self.no_full_key = text_value
				
		 
	self.part_text_set("play_key_icon", self.play_key)
	self.part_text_set("pause_key_icon", self.pause_key)
	self.part_text_set("stop_key_icon", self.stop_key)
	self.part_text_set("forward_key_icon", self.forw_key)
	self.part_text_set("backward_key_icon", self.backw_key)
	self.part_text_set("volume_m_key_icon", self.vol_m_key)
	self.part_text_set("volume_p_key_icon", self.vol_p_key)
	self.part_text_set("fullscreen_key_m_icon", self.full_key)
	self.part_text_set("no_fullscreen_key_m_icon", self.no_full_key)
	self.key_value = ""
	self.signal_emit("hide_screen_2", "")
	self.signal_emit("show_screen_1", "")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":

		self.main.remoko_conf.save_options()
		self.main.transition_to("multimedia")	

	elif source == "1":

		self.signal_emit("hide_screen_2", "")
		self.signal_emit("show_screen_1", "")

	elif source == "2":

		self.signal_emit("hide_screen_1", "")
		self.signal_emit("show_screen_2", "")
	
	else:
		
		if source == "play_key":

			self.key_value = self.part_text_get("play_key_icon")
			self.main.key_text = self.key_value

		elif source == "pause_key":

			self.key_value = self.part_text_get("pause_key_icon")
			self.main.key_text = self.key_value

		if source == "stop_key":

			self.key_value = self.part_text_get("stop_key_icon")
			self.main.key_text = self.key_value

		elif source == "forward_key":

			self.key_value = self.part_text_get("forward_key_icon")
			self.main.key_text = self.key_value

		if source == "backward_key":

			self.key_value = self.part_text_get("backward_key_icon")
			self.main.key_text = self.key_value

		elif source == "volume_m_key":

			self.key_value = self.part_text_get("volume_m_key_icon")
			self.main.key_text = self.key_value

		elif source == "volume_p_key":

			self.key_value = self.part_text_get("volume_p_key_icon")
			self.main.key_text = self.key_value


		elif source == "fullscreen_key_m":

			self.key_value = self.part_text_get("fullscreen_key_m_icon")
			self.main.key_text = self.key_value

		elif source == "no_fullscreen_key_m":

			self.key_value = self.part_text_get("no_fullscreen_key_m_icon")
			self.main.key_text = self.key_value

		self.main.current_conf_screen = "multimedia"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value"," "+self.key_value + " ")
		self.main.transition_to("conf_keys")	
	
#----------------------------------------------------------------------------#
class games(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")


#----------------------------------------------------------------------------#
class accelerometer(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "accelerometer")
	self.f = open("/dev/input/event3", "r")
	self.x = self.y = self.z = 0
	self.x_init = self.y_init = self.z_init = 0
	self.press = False
	self.first_time = True
	
	

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source == "conf_gestures":
		
		if self.press == False:
			self.press = True
			self.accell_value()
			self.first_time = False
			self.signal_emit("hold_pressed", "")

		else:
			self.press = False
			self.signal_emit("hold_released", "")
		
		#self.main.accelerometer_prev = "multimedia"
		#self.main.transition_to("accelerometer_conf")

        elif source == "button_right":
			
			self.main.connection.send_mouse_event(2,0,0,0)
			self.main.connection.send_event("btn_up")
			
	elif source == "button_left":
			
			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_event("btn_up")
			
	
				
	elif source == "button_middle":
			
			self.main.connection.send_mouse_event(4,0,0,0)
			self.main.connection.send_event("btn_up")

    def accell_value(self):
	   
	    #text = "x = %3d;  y = %3d;  z = %3d" % ( x, y, z )
	    maxx = maxy = maxz = 0
	    minx = miny = minz = 0

	    block = self.f.read(16)
	    if block[8] == "\x02":
		if block[10] == "\x00":
		   self.x = unpack_from( "@l", block[12:] )[0]
		  # maxx, minx = max( self.x, maxx ), min( self.x, minx )
		if block[10] == "\x01":
		   self.y = unpack_from( "@l", block[12:] )[0]
		   # maxy, miny = max( self.y, maxy ), min( self.y, miny )
		if block[10] == "\x02":
		   self.z = unpack_from( "@l", block[12:] )[0]
		  # maxz, minz = max( self.z, maxz ), min( self.z, minz )
		

	    #print "X=" + str(self.x) + " Y=" + str(self.y) + " Z=" + str(self.z)
	    if self.first_time == True:
		self.x_init = self.x
		self.y_init = self.y
		self.z_init = self.z

	    elif self.first_time == False:
		
		if self.y < 120 and self.x < 0:

			if (self.x- 10) > self.x_init:
				self.main.connection.send_mouse_event(00,2,0,00)
			
			elif self.x > -50:
				self.main.connection.send_mouse_event(00,-1,0,00)

			elif self.x > -200 and self.x < -100:
				self.main.connection.send_mouse_event(00,-2,0,00)
			
			elif self.x > -300 and self.x < -200:
				self.main.connection.send_mouse_event(00,-4,0,00)

			elif self.x > -400 and self.x < - 300:
				self.main.connection.send_mouse_event(00,-6,0,00)
			
			elif self.x > -500 and self.x < - 400:
				self.main.connection.send_mouse_event(00,-8,0,00)

			elif self.x > -600 and self.x < - 500:
				self.main.connection.send_mouse_event(00,-10,0,00)

			elif self.x > -700 and self.x < - 600:
				self.main.connection.send_mouse_event(00,-12,0,00)

			elif self.x < - 800:
				self.main.connection.send_mouse_event(00,-15,0,00)
			
		elif self.y > -130 and self.x > 150:


			if self.x < 250:
				self.main.connection.send_mouse_event(00,1,0,00)

			elif self.x > 250 and self.x < 350:
				self.main.connection.send_mouse_event(00,2,0,00)
			
			elif self.x > 350 and self.x < 450:
				self.main.connection.send_mouse_event(00,4,0,00)

			elif self.x > 450 and self.x < 550:
				self.main.connection.send_mouse_event(00,6,0,00)
			
			elif self.x > 550 and self.x < 650:
				self.main.connection.send_mouse_event(00,8,0,00)

			elif self.x > 650 and self.x < 750:
				self.main.connection.send_mouse_event(00,10,0,00)

			elif self.x > 750 and self.x < 850:
				self.main.connection.send_mouse_event(00,12,0,00)

			elif self.x >  950:
				self.main.connection.send_mouse_event(00,15,0,00)
			
			
			
		elif self.x < 120 and self.y < -100:

			if (self.y- 10) > self.y_init:
				self.main.connection.send_mouse_event(00,0,2,00)
			
			if self.y < -100 and self.y > -200:
				self.main.connection.send_mouse_event(00,0,-1,00)

			elif self.y < -200 and self.y > -300:
				self.main.connection.send_mouse_event(00,0,-2,00)
			
			elif self.y < -300 and self.y > -400:
				self.main.connection.send_mouse_event(00,0,-4,00)

			elif self.y < -400 and self.y > - 500:
				self.main.connection.send_mouse_event(00,0,-6,00)
			
			elif self.y < - 500 and self.y > - 600:
				self.main.connection.send_mouse_event(00,0,-8,00)

			elif self.y < -600 and self.y > - 700:
				self.main.connection.send_mouse_event(00,0,-10,00)

			elif self.y < -700 and self.y > -800:
				self.main.connection.send_mouse_event(00,0,-12,00)

			elif self.y < - 800:
				self.main.connection.send_mouse_event(00,0,-15,00)
			

		elif self.x < 190 and self.y > 120:

			#if (self.y- 10) < self.y_init:
			#	self.main.connection.send_mouse_event(00,0,-2,00)

			if self.y > 120 and self.y < 220:
				self.main.connection.send_mouse_event(00,0,1,00)

			elif self.y > 220 and self.y < 320:
				self.main.connection.send_mouse_event(00,0,2,00)
			
			elif self.y > 320 and self.y < 420:
				self.main.connection.send_mouse_event(00,0,4,00)

			elif self.y > 420 and self.y < 520:
				self.main.connection.send_mouse_event(00,0,6,00)
			
			elif self.y > 520 and self.y < 620:
				self.main.connection.send_mouse_event(00,0,8,00)

			elif self.y > 720 and self.y < 820:
				self.main.connection.send_mouse_event(00,0,10,00)

			elif self.y > 820 and self.y < 920:
				self.main.connection.send_mouse_event(00,0,12,00)

			elif self.y > 920:
				self.main.connection.send_mouse_event(00,0,15,00)
			
			
			
 
		self.x_init = self.x
		self.y_init = self.y
		self.z_init = self.z
		

		#print str(self.y) + "-" + str(self.y_init)
		
		
	    if self.press == True:
		ecore.timer_add(0.001,self.accell_value)

	    elif self.press == False:

		self.first_time = True
		
	    

#----------------------------------------------------------------------------#
class accelerometer_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "accelerometer_conf")
	count = 0
	self.up_key = ""
	self.up_down_key = ""
	self.right_key = ""
	self.right_left_key = ""
	self.left_key = ""
	self.left_right_key = ""
	self.down_key = ""
	self.down_up_key = ""
	self.forw_backw_key = ""
	self.shake_shake_key = ""
	self.z_key = ""
	self.horizontal_circle_key = ""

	for i in (self.main.up_key,self.main.up_down_key,self.main.right_key,self.main.right_left_key,self.main.left_key, self.main.down_key,self.main.down_up_key,self.main.left_right_key, self.main.forw_backw_key, self.main.shake_shake_key, self.main.z_key, self.main.horizontal_circle_key):

		if len(i) > 6:
			#shift translation
			if i[0] == "s":
				text_value = self.main.key_mapper.mapper[i]
				count +=1
		else:
			text_value = i
			count +=1
		if count == 1:
			self.up_key = text_value
		elif count == 2:
			self.up_down_key = text_value
		elif count == 3:
			self.right_key = text_value
		elif count == 4:
			self.right_left_key = text_value
		elif count == 5:
			self.left_key = text_value
		elif count == 6:
			self.left_right_key = text_value
		elif count == 7:
			self.down_key = text_value
		elif count == 8:
			self.down_up_key = text_value
		elif count == 9:
			self.forw_backw_key = text_value
		elif count == 10:
			self.shake_shake_key = text_value
		elif count == 11:
			self.z_key = text_value
		elif count == 12:
			self.horizontal_circle_key = text_value
				
		 
	self.part_text_set("up_key_icon", self.up_key)
	self.part_text_set("up_down_key_icon", self.up_down_key)
	self.part_text_set("right_key_icon", self.right_key)
	self.part_text_set("right_left_key_icon", self.right_left_key)
	self.part_text_set("left_key_icon", self.left_key)
	self.part_text_set("left_right_key_icon", self.left_right_key)
	self.part_text_set("down_key_icon", self.down_key)
	self.part_text_set("down_up_key_icon", self.down_up_key)
	self.part_text_set("forw_backw_key_icon", self.forw_backw_key)
	self.part_text_set("shake_shake_key_icon", self.shake_shake_key)
	self.part_text_set("z_key_icon", self.z_key)
	self.part_text_set("horizontal_circle_key_icon", self.horizontal_circle_key)
	
	self.key_value = ""
	if self.main.gestures == False:
		self.signal_emit("hide_screen_2", "")
		self.signal_emit("hide_screen_3", "")
		self.signal_emit("hide_screen_1", "")
		self.signal_emit("hide_screen_numbers","")
		self.part_text_set("label_gestures_off", "Gestures daemon isn't running")
	else:
		self.signal_emit("hide_screen_2", "")
		self.signal_emit("hide_screen_3", "")
		self.signal_emit("show_screen_1", "")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":

		self.main.remoko_conf.save_options()
		self.main.transition_to(self.main.accelerometer_prev)

	elif source == "1":

		self.signal_emit("hide_screen_2", "")
		self.signal_emit("hide_screen_3", "")
		self.signal_emit("show_screen_1", "")

	elif source == "2":

		self.signal_emit("hide_screen_1", "")
		self.signal_emit("hide_screen_3", "")
		self.signal_emit("show_screen_2", "")

	elif source == "3":
		
		self.signal_emit("hide_screen_1", "")
		self.signal_emit("hide_screen_2", "")
		self.signal_emit("show_screen_3", "")

	else:
		
		if source == "up_key":

			self.key_value = self.part_text_get("up_key_icon")
			self.main.key_text = self.key_value

		elif source == "up_down_key":

			self.key_value = self.part_text_get("up_down_key_icon")
			self.main.key_text = self.key_value

		if source == "right_key":

			self.key_value = self.part_text_get("right_key_icon")
			self.main.key_text = self.key_value

		elif source == "right_left_key":

			self.key_value = self.part_text_get("right_left_key_icon")
			self.main.key_text = self.key_value

		if source == "left_key":

			self.key_value = self.part_text_get("left_key_icon")
			self.main.key_text = self.key_value

		elif source == "left_right_key":

			self.key_value = self.part_text_get("left_right_key_icon")
			self.main.key_text = self.key_value

		elif source == "down_key":

			self.key_value = self.part_text_get("down_key_icon")
			self.main.key_text = self.key_value


		elif source == "down_up_key":

			self.key_value = self.part_text_get("down_up_key_icon")
			self.main.key_text = self.key_value

		elif source == "forw_back_key":

			self.key_value = self.part_text_get("forw_back_key_icon")
			self.main.key_text = self.key_value

		elif source == "shake_shake_key":

			self.key_value = self.part_text_get("shake_shake_key_icon")
			self.main.key_text = self.key_value

		elif source == "z_key":

			self.key_value = self.part_text_get("z_key_icon")
			self.main.key_text = self.key_value
		
		elif source == "horizontal_circle_key":

			self.key_value = self.part_text_get("horizontal_circle_key_icon")
			self.main.key_text = self.key_value

		self.main.current_conf_screen = "accelerometer_conf"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value"," "+self.key_value + " ")
		self.main.transition_to("conf_keys")	
#----------------------------------------------------------------------------#
class games(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games")
	self.f = open("/dev/input/event3", "r")
	self.x = self.y = self.z = 0
	self.x_init = self.y_init = self.z_init = 0
	self.press = False
	self.first_time = True
	self.send_event = False
	

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source ==	"conf_keys":
		

		if self.press == False:
			self.press = True
			self.accell_value()
			self.first_time = False
			self.signal_emit("hold_pressed", "")
			

		else:
			self.press = False
			self.signal_emit("hold_released", "")
			
		#self.main.transition_to("games_conf")

	elif source == "up":
	
		key = self.main.up_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "down":


		key = self.main.down_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "left":


		key = self.main.left_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "right":


		key = self.main.right_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "A":


		key = self.main.a_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)
	
	elif source == "B":


		key = self.main.b_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "C":


		key = self.main.c_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)

	elif source == "D":


		key = self.main.d_key
		modif, val = key_dec(self,key)
		value = self.main.key_mapper.mapper[str(val)]
		self.main.connection.send_keyboard_event(modif,value)


    def accell_value(self):

	    block = self.f.read(16)
	    if block[8] == "\x02":
		if block[10] == "\x00":
		   self.x = unpack_from( "@l", block[12:] )[0]
		  # maxx, minx = max( self.x, maxx ), min( self.x, minx )
		if block[10] == "\x01":
		   self.y = unpack_from( "@l", block[12:] )[0]
		   # maxy, miny = max( self.y, maxy ), min( self.y, miny )
		if block[10] == "\x02":
		   self.z = unpack_from( "@l", block[12:] )[0]
		  # maxz, minz = max( self.z, maxz ), min( self.z, minz )
	

	    #print "X=" + str(self.x) + " Y=" + str(self.y) + " Z=" + str(self.z)
	    if self.first_time == True:
		self.x_init = self.x
		self.y_init = self.y
		self.z_init = self.z

	    elif self.first_time == False:
	
		if self.x < -500:

			key = self.main.down_key
			modif, val = key_dec(self,key)
			value = self.main.key_mapper.mapper[str(val)]
			print "sending"
			self.main.connection.send_accel_event(modif,value)
		
		elif self.x > 500:
			key = self.main.up_key
			modif, val = key_dec(self,key)
			value = self.main.key_mapper.mapper[str(val)]
			print "sending"
			self.main.connection.send_accel_event(modif,value)
		elif self.y < -500:

			key = self.main.right_key
			modif, val = key_dec(self,key)
			value = self.main.key_mapper.mapper[str(val)]
			print "sending"
			self.main.connection.send_accel_event(modif,value)

		elif self.y > 500:

			key = self.main.left_key
			modif, val = key_dec(self,key)
			value = self.main.key_mapper.mapper[str(val)]
			print "sending"
			self.main.connection.send_accel_event(modif,value)
		else:
			self.main.connection.send_accel_event(0,0)
	
	    if self.press == True:
		ecore.timer_add(0.001,self.accell_value)

	    elif self.press == False:

		self.first_time = True
		
	    



#----------------------------------------------------------------------------#
class games_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games_conf")
	count = 0
	self.up_key = ""
	self.down_key = ""
	self.right_key = ""
	self.left_key = ""
	
	self.a_key = ""
	self.b_key = ""
	self.c_key = ""
	self.d_key = ""

	for i in (self.main.up_key,self.main.down_key,self.main.right_key,self.main.left_key,self.main.a_key,self.main.b_key, self.main.c_key, self.main.d_key):

		if len(i) > 6:
			#shift translation
			if i[0] == "s":
				text_value = self.main.key_mapper.mapper[i]
				count +=1

		elif len(i) > 5 and i[0] == "f" and i[1] == "n":
				val = str(i) + "+u"
				text_value = self.main.key_mapper.mapper[val]
				count +=1
		elif len(i) == 4 and i[0] == "s" and i[1] == "p":
				text_value = self.main.key_mapper.mapper[i]
				count +=1

		else:
			text_value = i
			count +=1
		if count == 1:
			self.up_key = text_value
		elif count == 2:
			self.down_key = text_value
		elif count == 3:
			self.right_key = text_value
		elif count == 4:
			self.left_key = text_value
		elif count == 5:
			self.a_key = text_value
		elif count == 6:
			self.b_key = text_value
		elif count == 7:
			self.c_key = text_value
		elif count == 8:
			self.d_key = text_value
				
		 
	self.part_text_set("up_key_icon", self.up_key)
	self.part_text_set("down_key_icon", self.down_key)
	self.part_text_set("right_key_icon", self.right_key)
	self.part_text_set("left_key_icon", self.left_key)
	self.part_text_set("a_key_icon", self.a_key)
	self.part_text_set("b_key_icon", self.b_key)
	self.part_text_set("c_key_icon", self.c_key)
	self.part_text_set("d_key_icon", self.d_key)
	
	
	
	self.signal_emit("hide_screen_2", "")
	self.signal_emit("show_screen_1", "")

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":

		self.main.remoko_conf.save_options()
		self.main.transition_to("games")

	elif source == "1":

		self.signal_emit("hide_screen_2", "")
		self.signal_emit("show_screen_1", "")

	elif source == "2":

		self.signal_emit("hide_screen_1", "")
		self.signal_emit("show_screen_2", "")

	else:
		
		if source == "up_key":

			self.key_value = self.part_text_get("up_key_icon")
			self.main.key_text = self.key_value

		elif source == "down_key":

			self.key_value = self.part_text_get("down_key_icon")
			self.main.key_text = self.key_value

		if source == "right_key":

			self.key_value = self.part_text_get("right_key_icon")
			self.main.key_text = self.key_value

		elif source == "left_key":

			self.key_value = self.part_text_get("left_key_icon")
			self.main.key_text = self.key_value

		if source == "a_key":

			self.key_value = self.part_text_get("a_key_icon")
			self.main.key_text = self.key_value

		elif source == "b_key":

			self.key_value = self.part_text_get("b_key_icon")
			self.main.key_text = self.key_value

		elif source == "c_key":

			self.key_value = self.part_text_get("c_key_icon")
			self.main.key_text = self.key_value


		elif source == "d_key":

			self.key_value = self.part_text_get("d_key_icon")
			self.main.key_text = self.key_value

		self.main.current_conf_screen = "games"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value + "  ")
		self.main.transition_to("conf_keys")	




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
	
        

    def initialize_remoko_server(self):

	if self.dbus_object.bluetooth_obj == True:

		self.connection = Connect()
		ecore.timer_add(1.0,self.connection.start_connection)
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


    def cbResourceChanged( self, resourcename ):
        for cb in self.onResourceChanged:
            cb( resourcename=resourcename )

    #def cbResourceChanged( self, resourcename, state, attributes ):
     #   for cb in self.onResourceChanged:
      #      cb( resourcename=resourcename, state=state, attributes=attributes )

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
            if ecore.evas.engine_type_supported_get("software_x11_16"):
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




