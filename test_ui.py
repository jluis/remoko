#!/usr/bin/env python

import evas
import ecore
import ecore.evas
import edje
import edje.decorators
import sys
import os

from remoko import *


class Screen(edje.Edje):
    def __init__(self, canvas, file):
        edje.Edje.__init__(self, canvas, file=file, group="layout")
        #self.container = Container(self.evas)
        #self.part_swallow("contents", self.container)

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def cb_on_btn_clicked(self, emission, source):
    	
    	if source == "bt_right":
    		
    		connection.send_event("02:04:000:000:000")
    		
    	elif source == "bt_left":
    		
    		connection.send_event("02:01:000:000:000")
    		
    	else:
    		
    		connection.send_event("quit")
    		connection.terminate_connection
    		
    		sys.exit(1)
        

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
