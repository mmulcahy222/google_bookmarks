from .state import *
from .context import *
from os import path 

class CopyToFileState(State):
	key = "c"
	def __init__(self):
		self.keymap = {
			"0": self.go_defaultstate,
		}
	def run(self):
		print("Copy into file")
	def file_put_contents(self,filename,data):
		f = open(filename, 'a')
		w = f.write(data)
		f.close()
		return w
	def save_to_file(self, text):
		bytes_written = self.file_put_contents("links_to_remove.txt",text + "\n")
		print(f"{bytes_written} bytes has been written in links_to_remove.txt")