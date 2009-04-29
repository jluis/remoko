import ConfigParser
import os


class remoko_conf:

	def __init__(self):

		self.config = ConfigParser.ConfigParser()
		
		try:
			
			self.config.readfp(open('settings.cfg'))
			try:
				#settings
				self.fullscreen = self.config.get("user","fullscreen")
				self.scroll = self.config.get("user","scroll")
				self.accelerometer = self.config.get("user","accelerometer")
				#presentation profile
				self.previous_key = self.config.get("presentation","previous_key")
				self.next_key = self.config.get("presentation","next_key")
				self.fullscreen_key = self.config.get("presentation","fullscreen_key")
				self.no_fullscreen_key = self.config.get("presentation","no_fullscreen_key")
				#multimedia profile
				self.play_key = self.config.get("multimedia","play_key")
				self.pause_key = self.config.get("multimedia","pause_key")
				self.stop_key = self.config.get("multimedia","stop_key")
				self.forward_key = self.config.get("multimedia","forward_key")
				self.backward_key = self.config.get("multimedia","backward_key")
				self.fullscreen_key_m = self.config.get("multimedia","fullscreen_key_m")
				self.volume_m_key = self.config.get("multimedia","volume_m_key")
				self.volume_p_key = self.config.get("multimedia","volume_p_key")
				self.no_fullscreen_key_m = self.config.get("multimedia", "no_fullscreen_key_m")
				#accelerometer profile
				self.up_key = self.config.get("accelerometer","up_key")
				self.up_down_key = self.config.get("accelerometer","up_down_key")
				self.right_key = self.config.get("accelerometer","right_key")
				self.right_left_key = self.config.get("accelerometer","right_left_key")
				self.left_key = self.config.get("accelerometer","left_key")
				self.left_right_key = self.config.get("accelerometer","left_right_key")
				self.down_key = self.config.get("accelerometer","down_key")
				self.down_up_key = self.config.get("accelerometer","down_up_key")
				self.forw_backw_key = self.config.get("accelerometer", "forw_backw_key")
				self.shake_shake_key = self.config.get("accelerometer","shake_shake_key")
				self.z_key = self.config.get("accelerometer","z_key")
				self.horizontal_circle_key = self.config.get("accelerometer", "horizontal_circle_key")
				#games profile
				self.up_key = self.config.get("games","up_key")
				self.down_key = self.config.get("games","down_key")
				self.right_key = self.config.get("games","right_key")
				self.left_key = self.config.get("games","left_key")
				self.a_key = self.config.get("games", "a_key")
				self.b_key = self.config.get("games","b_key")
				self.c_key = self.config.get("games","c_key")
				self.d_key = self.config.get("games", "d_key")
						
			except:
				print "ERROR: \'settings.ctg\' is damaged"
				#put some error, to show in the UI
				print "Error: Non such file or directory \'settings.cfg\'"
				self.fullscreen = "Yes"
				self.scroll = 0
				self.accelerometer = "Yes"
				self.previous_key = "Prior"
				self.next_key = "Next"
				self.fullscreen_key = "f5"
				self.no_fullscreen_key = "Escape"
				#multimedia profile
				self.play_key = "p"
				self.pause_key = "p"
				self.stop_key = "s"
				self.forward_key = "right"
				self.backward_key = "left"
				self.fullscreen_key_m = "f"
				self.volume_m_key = "minus"
				self.volume_p_key = "plus"
				self.no_fullscreen_key_m = "Escape"
				#accelerometer profile
				self.up_key = "f"
				self.up_down_key = "f5"
				self.right_key = "Next"
				self.right_left_key = "Right"
				self.left_key = "Prior"
				self.left_right_key = "Left"
				self.down_key = "d"
				self.down_up_key = "Escape"
				self.forw_backw_key = "b"
				self.shake_shake_key = "a"
				self.z_key = "s"
				self.horizontal_circle_key = "p"
				#games profile
				self.up_key = self.config.get("games","up_key")
				self.down_key = self.config.get("games","down_key")
				self.right_key = self.config.get("games","right_key")
				self.left_key = self.config.get("games","left_key")
				self.a_key = self.config.get("games", "a_key")
				self.b_key = self.config.get("games","b_key")
				self.c_key = self.config.get("games","c_key")
				self.d_key = self.config.get("games", "d_key")
						

		except:
			#put some error, to show in the UI
			print "Error: Non such file or directory \'settings.cfg\'"
			self.fullscreen = "Yes"
			self.scroll = 0
			self.accelerometer = "Yes"
			self.previous_key = "Prior"
			self.next_key = "Next"
			self.fullscreen_key = "f5"
			self.no_fullscreen_key = "Escape"
			#multimedia profile
			self.play_key = "p"
			self.pause_key = "p"
			self.stop_key = "s"
			self.forward_key = "right"
			self.backward_key = "left"
			self.fullscreen_key_m = "f"
			self.volume_m_key = "minus"
			self.volume_p_key = "plus"
			self.no_fullscreen_key_m = "Escape"
			#accelerometer profile
			self.up_key = "f"
			self.up_down_key = "f5"
			self.right_key = "Next"
			self.right_left_key = "Right"
			self.left_key = "Prior"
			self.left_right_key = "Left"
			self.down_key = "d"
			self.down_up_key = "Escape"
			self.forw_backw_key = "b"
			self.shake_shake_key = "a"
			self.z_key = "s"
			self.horizontal_circle_key = "p"
			#games profile
			self.up_key = self.config.get("games","up_key")
			self.down_key = self.config.get("games","down_key")
			self.right_key = self.config.get("games","right_key")
			self.left_key = self.config.get("games","left_key")
			self.a_key = self.config.get("games", "a_key")
			self.b_key = self.config.get("games","b_key")
			self.c_key = self.config.get("games","c_key")
			self.d_key = self.config.get("games", "d_key")
					


	def set_option(self,seccion,opt,value):
		
		self.config.set(seccion,opt, value)
		print "conf set"
		
	def save_options(self):	
	
		try:
			
			file = open('settings.cfg', 'w')
			self.config.write(file)
			file.close()
			print "Options saved"
			
		except:
			
			print "Error: Non such file or directory \'settings.cfg\'"

		
		


#cenas = remoko_conf()
#print cenas.fullscreen
#cenas.set_option("user", "fullscreen", "No")
