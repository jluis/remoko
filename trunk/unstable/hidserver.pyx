#
#      hidserver.pyx
#
#      Copyright 2008 -2009 Valerio Valerio <vdv100@gmail.com>
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


cdef extern from "hidserv.c":
    
    void init_server()
    int send_key_down(int modifiers, int val)
    int send_key_up()
    int send_mouse_event(int btn, int mov_x, int mov_y, int whell)
    int connection_state()
    int reconnect(char *src,char *dst)
    int quit_serv()
    void quit_thread()


def init_hidserver():

   init_server()
   

def send_key(mod, val):

   n = send_key_down(mod,val)
   return n

def release_key():

   n = send_key_up()
   return n

def send_mouse_ev(btn,mov_x,mov_y,whell):

  n = send_mouse_event(btn,mov_x,mov_y,whell)
  return n

def connec_state():

  n = connection_state()
  return n

def reConnect(src,dst):

  n = reconnect(src,dst)
  return n


def quit_server():
  
  n = quit_serv()
  return n

def quit():

  quit_thread()

