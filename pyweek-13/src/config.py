import logging
import optparse
import resource
try:
	import configparser as parser
except:
	import ConfigParser as parser

config = parser.ConfigParser()
config.read(resource.file_path('config.ini'))
get, getboolean, getint, getfloat = config.get, config.getboolean, config.getint, config.getfloat

def write():
	with open(resource.file_path('config.ini','w')) as configFile:
		config.write(configFile)

def parse_args():
	parser = optparse.OptionParser()
	parser.add_option("-v", "--debug",default=False, action='store_true',dest='debug',help="Print debugging information")
	parser.add_option("-p", "--profile",default=False, action='store_true',dest='profile',help="Profiling info")
	return parser.parse_args()

options,args = parse_args()

def setupLogging():
	if(options.debug):
		logLevel = logging.DEBUG
		format = '%(module)s:L%(lineno)04d| %(message)s'
	else:
		logLevel = logging.INFO
		format = '%(message)s'
	logging.basicConfig(level=logLevel,format=format)
