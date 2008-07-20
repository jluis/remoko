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


class Screen(edje.Edje):
    def __init__(self, canvas, file):
        edje.Edje.__init__(self, canvas, file=file, group="layout")
        self.x_init, self.y_init = 0,0
        self.mouse_down = False
        #self.container = Container(self.evas)
        #self.part_swallow("contents", self.container)
        
	
	#@edje.decorators.signal_callback("mouse,clicked,1", "*")
	#def cb_on_btn_clicked(self,emisson, source):
		
		#if source == "bt_right":
			
			#connection.send_event("02:02:000:000:000")
			
		#elif source == "bt_left":
			
			#connection.send_event("02:01:000:000:000")
			
			
		#elif source == "quit":
			
			#connection.send_event("quit")
			#connection.terminate_connection
			#ecore.main_loop_quit()
	
	#@edje.decorators.signal_callback("mouse,down,1", "*")
	#def on_mouse_over(self, emission, source):
		
		#print "Down Down"
				
	#@edje.decorators.signal_callback("mouse,up,1", "*")
	#def on_edje_signal_mouse_up_key(self, emission, source):
		
		#if self.mouse_down != None:
			#self.mouse_down = False
			#print "up up"
    	
	#@edje.decorators.signal_callback("mouse_area_pressed", "*")
	#def on_edje_signal_mouse_down_key(self, emission, source):
		#self.mouse_down = True
		#print "cenas"
		
	#@edje.decorators.signal_callback("mouse,move", "*")
	#def on_mouse_down(self, emission, source):
		#self.mouse_down = True
		#print "cenas2"

    @edje.decorators.signal_callback("mouse,down,1", "*")
    def on_mouse_down(self, emission, source):
		
		self.mouse_down = True

    @edje.decorators.signal_callback("mouse,up,1", "*")
    def on_mouse_up(self, emission, source):
		
		self.mouse_down = False
		self.x_init, self.y_init = 0,0

    @edje.decorators.signal_callback("mouse_over_area", "*")
    def on_mouse_move(self, emission, source):

		if self.mouse_down == True:
			x,y = canvas.pointer_canvas_xy
			x1,y1 = mouse_position(self,x,y)

			print x1
			print y1
				
			mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
			print mov
			connection.send_event(mov)

		else:

			print "333"
	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_mouse_over(self, emission, source):
    	
		print self.mouse_down
		if source == "bt_right":
			print "bt"
			connection.send_event("02:02:000:000:000")
			
		elif source == "bt_left":
			
			print "bt_l"
			connection.send_event("02:01:000:000:000")
			
			
		elif source == "quit":
			
			connection.send_event("quit")
			connection.terminate_connection
			ecore.main_loop_quit()
				
		else:
				
			pass
												
connection = Connect()
while connection.connect == False:
	
	print "Waiting"

w, h = 480, 640
ee = ecore.evas.SoftwareX11(w=w, h=h)

# Load and setup UI
ee.title = "Remoko test"
canvas = ee.evas
edje_file = os.path.join(os.path.dirname(sys.argv[0]), "01-swallow.edj")

screen = Screen(canvas, edje_file)
screen.size = canvas.size
screen.show()
ee.data["screen"] = screen

ee.show()
ecore.main_loop_begin()

