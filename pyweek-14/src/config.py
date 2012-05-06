'''Process command line options and config files'''
import logging
import optparse
import resource
try:
	from configparser import ConfigParser
except ImportError:
	from ConfigParser import ConfigParser

class Settings(ConfigParser):
	'''Stores any tweakable settings or savable preferences'''
	def __init__(self):
		ConfigParser.__init__(self)
		self.reload()

	def reload(self):
		'''Reload the config file'''
		self.read(resource.file_path('config.ini'))

def parse_args():
	'''Parse command line arguments'''
	parser = optparse.OptionParser()

	parser.add_option("-v", "--debug", default=False, action='store_true',
			dest='debug', help="Print debugging information")

	return parser.parse_args()

def setupLogging():
	'''Set up the logger, taking into account the -v option'''
	if(options.debug):
		logLevel = logging.DEBUG
		fmt = '%(module)s:L%(lineno)04d| %(message)s'
	else:
		logLevel = logging.INFO
		fmt = '%(message)s'
	logging.basicConfig(level=logLevel, format=fmt)

settings = Settings()
options, args = parse_args()
