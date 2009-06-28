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

	
    def onShow( self ):
	self.focus = True
    

    def onHide( self ):
	self.focus = False

    @edje.decorators.signal_callback("mouse,clicked,1", "*")
    def on_edje_signal_button_pressed(self, emission, source):
	if source == "back":
		
		self.main.transition_to("menu")

	elif source == "racing":

		self.main.transition_to("games_racing")
		

	elif source == "ball":

		self.main.transition_to("games_ball")

	elif source == "fullscreen":

		key = self.main.fullscreen_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)

	elif source == "no_fullscreen":

		key = self.main.no_fullscreen_key
		modif, val = key_dec(self,key)

		self.main.connection.send_keyboard_event(modif,val)


