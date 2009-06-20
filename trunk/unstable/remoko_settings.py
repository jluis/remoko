#
#      remoko_settings.py
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


    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False

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

