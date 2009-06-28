#
#      remoko_games_ball.py
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
import time
from struct import unpack_from
from remoko_edje_group import *

#----------------------------------------------------------------------------#
class games_ball(edje_group):
#----------------------------------------------------------------------------#
    def __init__(self, main):
        edje_group.__init__(self, main, "games_ball")
	self.f = open("/dev/input/event3", "r")
	self.x = self.y = self.z = 0
	self.x_init_a = self.y_init_a = self.z_init_a = 0
	self.first_time = True
	self.accel_on = False
	self.tape_mouse_area = 0
	self.x_init, self.y_init = 0,0
        self.mouse_down = False
        self.first_touch = True
	
	
    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False
        

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("games")

	elif source ==	"accel_button":
		

		if not self.accel_on:
			self.accel_on = True
			self.accell_value()
			self.first_time = False
			self.signal_emit("accel_on", "")
			

		else:
			self.accel_on = False
			self.signal_emit("accel_off", "")
		

        elif source == "button_right":
			
			self.main.connection.send_mouse_event(2,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)
			
	elif source == "button_left":
			
			self.main.connection.send_mouse_event(1,0,0,0)
			self.main.connection.send_mouse_event(0,0,0,0)
			
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
				
				x_m,y_m = self.main.canvas.pointer_canvas_xy
				x1,y1 = mouse_position(self,x_m,y_m)
					
				self.main.connection.send_mouse_event(00,x1,y1,00)

		else:
			pass	


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
	    if self.first_time:
		self.x_init_a = self.x
		self.y_init_a = self.y
		self.z_init_a = self.z

	    elif not self.first_time:
		
		if self.y < 120 and self.x < 0:

			#print "XXXX"

			#if (self.x- 10) > self.x_init_a:
			#	self.main.connection.send_mouse_event(00,2,0,00)
			
			#elif self.x > -50:
			#	self.main.connection.send_mouse_event(00,-2,0,00)

			if self.x > -100:

				self.main.connection.send_mouse_event(00,-1,0,00)

			elif self.x < -100:

				self.main.connection.send_mouse_event(00,-2,0,00)
			
			#elif self.x > -300 and self.x < -200:
			#	self.main.connection.send_mouse_event(00,-4,0,00)

			#elif self.x > -400 and self.x < - 300:
			#	self.main.connection.send_mouse_event(00,-6,0,00)
			
			#elif self.x > -500 and self.x < - 400:
			#	self.main.connection.send_mouse_event(00,-8,0,00)

			#elif self.x > -600 and self.x < - 500:
			#	self.main.connection.send_mouse_event(00,-10,0,00)

			#elif self.x > -700 and self.x < - 600:
			#	self.main.connection.send_mouse_event(00,-12,0,00)

			#elif self.x < - 800:
			#	self.main.connection.send_mouse_event(00,-15,0,00)
			
		elif self.y > -130 and self.x > 150:


			if self.x < 250:
				self.main.connection.send_mouse_event(00,1,0,00)

			elif self.x > 250:
				self.main.connection.send_mouse_event(00,2,0,00)
			
			#elif self.x > 350 and self.x < 450:
			#	self.main.connection.send_mouse_event(00,4,0,00)

			#elif self.x > 450 and self.x < 550:
			#	self.main.connection.send_mouse_event(00,6,0,00)
			
			#elif self.x > 550 and self.x < 650:
			#	self.main.connection.send_mouse_event(00,8,0,00)

			#elif self.x > 650 and self.x < 750:
			#	self.main.connection.send_mouse_event(00,10,0,00)

			#elif self.x > 750 and self.x < 850:
			#	self.main.connection.send_mouse_event(00,12,0,00)

			#elif self.x >  950:
				#self.main.connection.send_mouse_event(00,15,0,00)
			
			
			
		elif self.x < 120 and self.y < -100:

			#if (self.y- 10) > self.y_init_a:
			#	self.main.connection.send_mouse_event(00,0,2,00)
			
			if self.y < -100 and self.y > -200:
				self.main.connection.send_mouse_event(00,0,1,00)

			elif self.y < -200:
				self.main.connection.send_mouse_event(00,0,2,00)
			
			#elif self.y < -300 and self.y > -400:
			#	self.main.connection.send_mouse_event(00,0,-4,00)

			#elif self.y < -400 and self.y > - 500:
			#	self.main.connection.send_mouse_event(00,0,-6,00)
			
			#elif self.y < - 500 and self.y > - 600:
			#	self.main.connection.send_mouse_event(00,0,-8,00)

			#elif self.y < -600 and self.y > - 700:
			#	self.main.connection.send_mouse_event(00,0,-10,00)

			#elif self.y < -700 and self.y > -800:
			#	self.main.connection.send_mouse_event(00,0,-12,00)

			#elif self.y < - 800:
			#	self.main.connection.send_mouse_event(00,0,-15,00)
			

		elif self.x < 190 and self.y > 120:

			#if (self.y- 10) < self.y_init_a:
			#	self.main.connection.send_mouse_event(00,0,-2,00)

			if self.y < 220:
				self.main.connection.send_mouse_event(00,0,-1,00)

			elif self.y > 220:
				self.main.connection.send_mouse_event(00,0,-2,00)
			
			#elif self.y > 320 and self.y < 420:
			#	self.main.connection.send_mouse_event(00,0,4,00)

			#elif self.y > 420 and self.y < 520:
			#	self.main.connection.send_mouse_event(00,0,6,00)
			
			#elif self.y > 520 and self.y < 620:
			#	self.main.connection.send_mouse_event(00,0,8,00)

			#elif self.y > 720 and self.y < 820:
			#	self.main.connection.send_mouse_event(00,0,10,00)

			#elif self.y > 820 and self.y < 920:
			#	self.main.connection.send_mouse_event(00,0,12,00)

			#elif self.y > 920:
			#	self.main.connection.send_mouse_event(00,0,15,00)
			
			
			
 
		self.x_init_a = self.x
		self.y_init_a = self.y
		self.z_init_a = self.z
		

		#print str(self.y) + "-" + str(self.y_init_a)
		
		
	    if self.accel_on:
		ecore.timer_add(0.001,self.accell_value)

	    elif not self.accel_on:

		self.first_time = True
		
