#
#      remoko_games_racing.py
#
#      Copyright 2008 -2009 	Valerio Valerio <vdv100@gmail.com>
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



import e_dbus
import evas
import evas.decorators
import edje
import edje.decorators
import ecore
import ecore.x
import ecore.evas
from struct import unpack_from
from remoko_edje_group import *


#----------------------------------------------------------------------------#
class games_racing(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games_racing")
	self.f = open("/dev/input/event3", "r")
	self.x = self.y = self.z = 0
	self.x_init = self.y_init = self.z_init = 0
	self.x_tmp = self.y_tmp = self.z_tmp = 0
	self.accel_on = False
	self.first_time = True
	self.send_event = False
	self.pass_event = False
	self.pass_event2 = False
	self.counter = 0
	self.a_pressed = False

	
    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False


    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_edje_signal_button_released(self, emission, source):

	if source =="back" or source == "conf_keys":
		pass
	else:
		self.main.connection.release_keyboard_event()
		self.a_pressed = False


    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("games")

	elif source ==	"accel_button":
		

		if not self.accel_on:
			self.accel_on = True
			self.accel_cb()
			self.accell_value()
			self.first_time = False
			self.signal_emit("accel_on", "")
			

		else:
			self.accel_on = False
			self.signal_emit("accel_off", "")

	elif source ==	"conf_keys":
		
		self.main.transition_to("games_racing_conf")		
	

	elif source == "a":


		key = self.main.a_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)
		self.a_pressed = True
	
	elif source == "b":


		key = self.main.b_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "c":


		key = self.main.c_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "d":


		key = self.main.d_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)


    def accel_cb(self):

	    text = "x = %3d;  y = %3d;  z = %3d" % ( 0, 0, 0 )
	    counter = 0
	    block = self.f.read(16)
	    if block[8] == "\x02":
		if block[10] == "\x00":
		   self.x_tmp = unpack_from( "@l", block[12:] )[0]
		if block[10] == "\x01":
		   self.y_tmp = unpack_from( "@l", block[12:] )[0]
		if block[10] == "\x02":
		   self.z_tmp = unpack_from( "@l", block[12:] )[0]
		#text = "x = %3d;  y = %3d;  z = %3d" % ( self.x_tmp, self.y_tmp, self.z_tmp) 

	    if counter % 5 == 0:
	    	self.x = self.x_tmp
		self.y = self.y_tmp
		self.z = self.z_tmp
		#print ("Values: %s" % text)
	    counter = counter + 1
	    if self.accel_on:
		ecore.timer_add(0.0,self.accel_cb)		


    def accell_value(self):
	 	    

	if self.send_event:

		self.main.connection.release_keyboard_event()
		self.send_event = False
		key = self.main.a_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)
		
		print "release"
	else:

		if self.pass_event:
			self.pass_event = False
		else:

			self.pass_event2 = False
			
		#print "released"
	
		#if self.x < -500:

		#	key = self.main.down_key
		#	modif, val = key_dec(self,key)
		#	value = self.main.key_mapper.mapper[str(val)]
		#	print "sending"
		#	self.main.connection.send_accel_event(modif,value)
		
		#elif self.x > 500:
		#	key = self.main.up_key
		#	modif, val = key_dec(self,key)
		#	value = self.main.key_mapper.mapper[str(val)]
		#	print "sending"
		#	self.main.connection.send_accel_event(modif,value)
	if self.y < -400:

			key = self.main.right_key
			modif, val = key_dec(self,key)

			self.main.connection.send_keyboard_event(modif,val)
			self.send_event = True

	elif self.y > 400:

			key = self.main.left_key
			modif, val = key_dec(self,key)
	
			self.main.connection.send_keyboard_event(modif,val)
			self.send_event = True

	if not self.pass_event:

		if self.y < -200:

			key = self.main.right_key
			modif, val = key_dec(self,key)
			print "->>>>>>>>"
			self.main.connection.send_keyboard_event(modif,val)
			self.send_event = True
			self.pass_event = True

		elif self.y > 200:

			key = self.main.left_key
			modif, val = key_dec(self,key)
	
			self.main.connection.send_keyboard_event(modif,val)
			self.send_event = True
			self.pass_event = True			
	
	if self.accel_on:
		ecore.timer_add(0.10,self.accell_value)

	elif not self.accel_on:

		self.first_time = True


#----------------------------------------------------------------------------#
class games_racing_conf(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games_racing_conf")
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
		self.main.transition_to("games_racing")

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

		self.main.current_conf_screen = "games_racing"
		self.main.current_source = source
		self.main.groups["conf_keys"].part_text_set("value","  "+self.key_value + "  ")
		self.main.transition_to("conf_keys")	



		
	    


