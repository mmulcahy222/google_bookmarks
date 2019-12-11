from .state import *
import copy
from copy import *
import pprint
import json
import re

class RemoveBookmarkState(State):
	
	key = "r"
	bookmarks_file_path = 'C:/Users/goon/AppData/Local/Google/Chrome/User Data/Default/Bookmarks'
	links_to_delete_path = 'C:/makeshift/files/google_bookmarks/links_to_remove.txt'
	links_gone = []
	def __init__(self):
		self.keymap = {
			"0": self.go_defaultstate,
			"1": self.run
		}

	def search_structure(self,structure, search='',depth=-1):
		list_of_keys = None
		def recurse(structure, path=[], search=''):
			nonlocal list_of_keys
			if isinstance(structure, dict):
				for k, value in structure.items():
					path.append(k)
					recurse(value, path=path, search=search)
					path.pop()
			elif isinstance(structure, list):
				for i, value in enumerate(structure):
					path.append(i)
					recurse(value, path=path, search=search)
					path.pop()
			if str(search) == str(structure):
				list_of_keys = copy(path)
		recurse(structure,search=search)
		list_of_keys = list_of_keys[0:depth]
		for key in list_of_keys:
			structure = structure[key]
		return structure
	def run(self):
		#read google bookmarks
		fs = open(self.bookmarks_file_path,'r', encoding='utf-8', errors='ignore')
		filedata = fs.read()
		fs.close()
		self.bookmarks_structure = eval(filedata)
		#get the regex to find the links to rid of (self.extract_links_to_delete)
		regex_pattern_link_chunks = self.extract_links_to_delete()
		requested_structure = self.search_structure(self.bookmarks_structure,search="",depth=-1)
		requested_structure_nodes = requested_structure['children']
		print("There were {} nodes in here".format(len(requested_structure_nodes)))
		for k,node in enumerate(requested_structure_nodes):
			url = node['url']
			if re.search(regex_pattern_link_chunks,url):
				print(f"{url} is gone")
				del requested_structure_nodes[k]
			else:
				pass #print(url, "No")
		print("There are now {} nodes in here".format(len(requested_structure['children'])))
		#SAVE IN THIS METHOD
		self.save_new_bookmarks()
	def save_new_bookmarks(self):
		fd = open(self.bookmarks_file_path,'w', encoding='utf-8', errors='ignore')
		bookmarks_repaired_neat_string = json.dumps(self.bookmarks_structure, indent = 4)
		fd.write(bookmarks_repaired_neat_string)
		fd.close()
	def extract_relevant_token(self,text):
		try:
			#three variations
			result = re.findall('(?<=com\/).*(?=\?)|(?<=com\/).*$|(?<=\?id=)\d*',text)[-1]
			return result.strip()
		except KeyError:
			print("Key Error")
	def extract_links_to_delete(self):
		fs = open(self.links_to_delete_path,'r', encoding='utf-8', errors='ignore')
		for line in fs.readlines():
			self.links_gone.append(self.extract_relevant_token(line))
		fs.close()
		#turn those links that were COPIED from links_to_remove.txt into a regex pattern
		regex_pattern_link_chunks = '|'.join(self.links_gone)
		regex_pattern_link_chunks = regex_pattern_link_chunks.replace('.','\.')
		return regex_pattern_link_chunks
