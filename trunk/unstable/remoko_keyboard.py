#
#      remoko_keyboard.py
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



import time
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

    @evas.decorators.key_up_callback
    def key_up_cb( self, event ):
	self.main.connection.release_keyboard_event()
        key = event.keyname

	if key == "Shift_L":
		self.shift = False

	elif key == "Alt_L":
		self.alt = False

	elif key == "Control_L":
		self.ctrl = False

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
			
			if self.shift:
				self.main.connection.send_keyboard_event("02",value)
				self.shift = False
			
			elif self.alt  and self.ctrl:
				self.main.connection.send_keyboard_event("05",value)
				self.ctrl = False
				self.alt = False
				
			elif self.ctrl:
				self.main.connection.send_keyboard_event("01",value)
				self.ctrl = False
				
			elif self.alt:
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
			self.main.connection.send_mouse_event(0,0,0,0)	

		self.mouse_down = False
		self.first_touch = True
		self.x_init, self.y_init = 0,0

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_over_area(self, emission, source):

		if self.mouse_down:
			
			if self.first_touch:
				
				self.first_touch = False
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)
					
				mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
				self.main.connection.send_mouse_event(00,x1,y1,00)

		else:
			pass	


