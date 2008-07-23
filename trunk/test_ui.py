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

import os
import sys
import time
import evas
import evas.decorators
import edje
import edje.decorators
import ecore
import ecore.evas
from optparse import OptionParser

from remoko import *

WIDTH = 480
HEIGHT = 640

TITLE = "remoko"
WM_NAME = "remoko"
WM_CLASS = "remoko"

edjepaths = "remoko.edj".split()

for i in edjepaths:
    if os.path.exists( i ):
       global edjepath
       edjepath = i
       break
else:
    raise Exception( "zhone.edj not found. looked in %s" % edjepaths )



def mouse_position(self,x1,y1):
	
	x = x1 - self.x_init
	y = y1 - self.y_init
	
	self.x_init = x1
	self.y_init = y1
			
	return x,y

#----------------------------------------------------------------------------#
class edje_group(edje.Edje):
#----------------------------------------------------------------------------#
    def __init__(self, main, group, parent_name="main"):
        self.main = main
        self.parent_name = parent_name
        global edjepath
        print edjepath
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
	self.part_text_set("label_connect", "waiting ")
	ecore.timer_add(3.0,self.main.transition_to,"mouse_ui")
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	print "apssou"
        self.main.transition_to(source)


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

				tmp,self.scroll_pos = self.main.canvas.pointer_canvas_xy			
				self.first_touch = False
			else:

				tmp,y_scroll = self.main.canvas.pointer_canvas_xy	

				if y_scroll > self.scroll_pos:

					self.scroll_pos = y_scroll
					#connection.send_event("02:00:000:000:001")
					print "Scroll_down"

				elif y_scroll < self.scroll_pos:

					self.scroll_pos = y_scroll
					#connection.send_event("02:00:000:000:255")
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
				self.x_init, self.y_init = self.main.canvas.pointer_canvas_xy
				
			else:
				
				x,y = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x,y)

				print x1
				print y1
				
				if self.button_hold == True:
					
					mov = "02:01:" + str(x1) + ":" + str(y1) + ":000"
					print mov
					#connection.send_event(mov)
					
				else:	
					
					mov = "02:00:" + str(x1) + ":" + str(y1) + ":000"
					print mov
					#connection.send_event(mov)

		else:

			print "333"

   
	
    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_mouse_over(self, emission, source):
    	
		print self.mouse_down
		if source == "bt_right_icon":
			print "bt"
			#connection.send_event("02:02:000:000:000")
			
		elif source == "bt_left_icon":
			
			print "bt_l"
			#connection.send_event("02:01:000:000:00")
			
		elif source == "bt_hold_icon":
			
			if self.button_hold == True:
				
				self.button_hold = False
				
				self.signal_emit("hold_released", "")
				
			else:
				
				self.button_hold = True
				self.signal_emit("hold_pressed", "")
				
		elif source == "bt_middle_icon":
			
			print "bt_m"
			#connection.send_event("02:04:000:000:000")
			
			
		elif source == "back_icon":
	
			#connection.terminate_connection()
			#ecore.main_loop_quit()
			print self.main.previous_group
			self.main.transition_to("main")
				
		else:
				
			pass
			
			
												
#connection = Connect()
#while connection.connect == False:
	
	#print "Waiting ..."





#----------------------------------------------------------------------------#
class GUI(object):
#----------------------------------------------------------------------------#
    def __init__( self, options, args ):

        edje.frametime_set(1.0 / options.fps)

        self.evas_canvas = EvasCanvas(
            fullscreen = options.fullscreen,
            engine = options.engine,
            size = options.geometry
        )
	
	self.canvas = self.evas_canvas.evas_obj.evas

        self.groups = {}

        self.groups["swallow"] = edje_group(self, "swallow")
        self.evas_canvas.evas_obj.data["swallow"] = self.groups["swallow"]

        for page in ("main","mouse_ui", "connect_to"):
		ctor = globals().get( page, None )
		print ctor
		if ctor:
			self.groups[page] = ctor( self )
			self.evas_canvas.evas_obj.data[page] = self.groups[page]


        self.groups["swallow"].show()

        self.groups["swallow"].part_swallow("area1", self.groups["main"])
        self.current_group = self.groups["main"]
        self.previous_group = self.groups["mouse_ui"]
        self.in_transition = False

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




