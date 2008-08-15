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
		except:
			#put some error, to show in the UI
			print "Error: Non such file or directory \'settings.cfg\'"
			self.fullscreen = "Yes"
			self.scroll = 0
			self.previous_key = "Prior"
			self.next_key = "Next"
			self.fullscreen_key = "f5"
			self.no_fullscreen_key = "Escape"

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

		
		
