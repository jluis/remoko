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
				
			except:
				print "ERROR: \'settings.ctg\' is damaged"
				#put some error, to show in the UI
				print "Error: Non such file or directory \'settings.cfg\'"
				self.fullscreen = "Yes"
				self.scroll = 0
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
		except:
			#put some error, to show in the UI
			print "Error: Non such file or directory \'settings.cfg\'"
			self.fullscreen = "Yes"
			self.scroll = 0
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
