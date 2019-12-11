class State:
	keymap = {}
	def __init__(self):
		pass
	def run(self):
		pass
	def go_defaultstate(self):
		#corresponds to the name of the directory of states in Context
		self._context.set_state('defaultstate')
	def __getattr__(*args, **kwargs):
		return lambda *args:None
