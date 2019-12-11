from .state import *

class DefaultState(State):
	key = "d"
	def __init__(self):
		self.keymap = {
			"0": self.go_defaultstate,
			"1": self.go_copytofilestate,
			"2": self.go_removebookmarkstate
		}
	def run(self):
		print("Default")
	#Default State is in the 
	def go_copytofilestate(self):
		self._context.set_state('copytofilestate')
	def go_exitstate(self):
		self._context.set_state('exitstate')
	def go_removebookmarkstate(self):
		self._context.set_state('removebookmarkstate')
