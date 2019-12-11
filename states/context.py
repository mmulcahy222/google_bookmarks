from .state import *
from .singletonmeta import *
#subclasses must be put here 
from .copytofilestate import *
from .defaultstate import *
from .exitstate import *
from .removebookmarkstate import *
class Context:
	def __init__(self):
		self.state_directory = {i.__name__.lower():i() for i in State.__subclasses__()}
		#since the state objects are created upon the instantiation of context, we got to put in the context for all of them to enable two-way communication & two-way coupling. The purpose of this is to change the state to another state inside a state object
		for _,state in self.state_directory.items():
			state._context = self
	def set_state(self,state_name):
		#This does the transition. This looks at the name directory of the directory above (with single class objects) and picks out the class, so it doesn't make a new class for each transition. A waste of memory if adding in new class objects.
		self._state = self.state_directory.get(state_name.lower(),self.state_directory['defaultstate'])
		#There is a two way communication/coupling/composition between context/object and the state. Context has state, state has context (below). The reason is because we're changing states inside the state itself.
		self.print_banner()
	def process_keystroke(self,keystroke):
		print(f"You pressed {keystroke}")
		keymap_function = self._state.keymap.get(keystroke,lambda:print("Pick something in the menu"))
		keymap_function()
	def print_banner(self):
		print()
		current_state_name = self._state.__class__.__name__
		print(f"You are in {current_state_name}")
		print("+" * 3 + "-" * 20 + "+" * 3)
		print("{:10s} {:10s}".format("Key","Action"))
		print("+" * 3 + "-" * 20 + "+" * 3)
		for keyboard_char,state_instance in self._state.keymap.items():
			print("{:10s} {:10s}".format(keyboard_char,state_instance.__name__))
		print()
	def __getattr__(self, name):
		'''
		Just like Variable Functions in PHP, it will call the proper function based on the name
		If the function doesn't exist at it, it will call the __getattr__ function in the context, then __getattr__ function in the state
		'''
		return getattr(self._state,name)