import ConfigParser
import os


class remoko_conf:

	def __init__(self):

		self.config = ConfigParser.ConfigParser()
		
		try:
			
			self.config.readfp(open('settings.cfg'))
			self.fullscreen = self.config.get("user","fullscreen")
			self.scroll = self.config.get("user","scroll")
			
		except:
			#put some error, to show in the UI
			print "Error: Non such file or directory"
			self.fullscreen = "Yes"
			self.scroll = 0

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
			
			print "Error: Non such file or directory"

		
		


#cenas = remoko_conf()
#print cenas.fullscreen
#cenas.set_option("user", "fullscreen", "No")
