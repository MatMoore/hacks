import os
import sys

def data_path():
	return os.path.join(script_dir(), 'data')

def file_path(filename):
	return os.path.join(data_path(), filename)

def script_dir():
	return os.path.abspath(os.path.dirname(sys.argv[0]))
