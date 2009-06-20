#
#      remoko_accelerometer.py
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
class accelerometer(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "accelerometer")
	self.f = open("/dev/input/event3", "r")
	self.x = self.y = self.z = 0
	self.x_init = self.y_init = self.z_init = 0
	self.press = False
	self.first_time = True
	
	
    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False
        

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
			self.main.connection.send_mouse_event(0,0,0,0)
			
	elif source == "button_left":
			
			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)
			
	
				
	elif source == "button_middle":
			
			self.main.connection.send_mouse_event(4,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)

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
