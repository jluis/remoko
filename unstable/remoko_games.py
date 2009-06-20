#
#      remoko_games.py
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
from remoko_edje_group import *


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

	
    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False

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

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "down":


		key = self.main.down_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "left":


		key = self.main.left_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "right":


		key = self.main.right_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "A":


		key = self.main.a_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)
	
	elif source == "B":


		key = self.main.b_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "C":


		key = self.main.c_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "D":


		key = self.main.d_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)


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



