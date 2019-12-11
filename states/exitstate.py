from .state import *
import sys

class ExitState(State):
	key = "e"
	def run(self):
		sys.exit(0)