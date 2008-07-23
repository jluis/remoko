#
#      test_ui.py
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

#!/usr/bin/env python

import evas
import evas.decorators
import ecore
import ecore.evas
import edje
import edje.decorators
import sys
import os

from remoko import *

def mouse_position(self,x1,y1):
	
	x = x1 - self.x_init
	y = y1 - self.y_init
	
	self.x_init = x1
	self.y_init = y1
			
	return x,y


class Mouse_ui(edje.Edje):
    def __init__(self, canvas, file):
        edje.Edje.__init__(self, canvas, file=file, group="mouse_ui")
        self.x_init, self.y_init = 0,0
        self.mouse_down = False
        self.first_touch = True
        self.button_hold = False
	self.scroll_pos = 0
        #self.container = Container(self.evas)
        #self.part_swallow("contents", self.container)

    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_mouse_down(self, emission, source):
		
		self.mouse_down = True

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_mouse_up(self, emission, source):
		
		self.mouse_down = False
		self.first_touch = True
		self.x_init, self.y_init = 0,0

    @edje.decorators.signal_callback("mouse_over_scroll", "*") 
    def on_mouse_over_scroll(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:

				tmp,self.scroll_pos = canvas.pointer_canvas_xy			
				self.first_touch = False
			else:

				tmp,y_scroll = canvas.pointer_canvas_xy	

				if y_scroll > self.scroll_pos:

					self.scroll_pos = y_scroll
					connection.send_event("02:00:000:000:001")
					print "Scroll_down"

				elif y_scroll < self.scroll_pos:

					self.scroll_pos = y_scroll
					connection.send_event("02:00:000:000:255")
					print "Scroll_up"
				else:

					pass

		else:

			print "mouse_over_scroll"

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_over_area(self, emission, source):

		if self.mouse_down == True:
			
			if self.first_touch == True:
				
				self.first_touch = False
				self.x_init, self.y_init = canvas.pointer_canvas_xy
				
			else:
				
				x,y = canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)

				print x1
				print y1
				
				if self.button_hold == True:
					
					mov = "02:01:" + str(x1) + ":" + str(y1) + ":000"
					print mov
					connection.send_event(mov)
					
				else:	
					
					mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
					print mov
					connection.send_event(mov)

		else:

			print "333"

   
	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_mouse_over(self, emission, source):
    	
		print self.mouse_down
		if source == "bt_right_icon":
			print "bt"
			connection.send_event("02:02:000:000:000")
			
		elif source == "bt_left_icon":
			
			print "bt_l"
			connection.send_event("02:01:000:000:00")
			
		elif source == "bt_hold_icon":
			
			if self.button_hold == True:
				
				self.button_hold = False
				
				self.signal_emit("hold_released", "")
				
			else:
				
				self.button_hold = True
				self.signal_emit("hold_pressed", "")
				
		elif source == "bt_middle_icon":
			
			print "bt_m"
			connection.send_event("02:04:000:000:000")
			
			
		elif source == "quit_icon":
	
			connection.terminate_connection()
			ecore.main_loop_quit()
				
		else:
				
			pass
			
			
												
connection = Connect()
while connection.connect == False:
	
	print "Waiting ..."

w, h = 480, 640
ee = ecore.evas.SoftwareX11(w=w, h=h)

# Load and setup UI
ee.title = "Remoko"
canvas = ee.evas
edje_file = os.path.join(os.path.dirname(sys.argv[0]), "remoko_mouse.edj")

screen = Mouse_ui(canvas, edje_file)

screen.size = canvas.size
screen.show()
ee.data["screen"] = screen

ee.fullscreen = not ee.fullscreen
ee.show()
ecore.main_loop_begin()

