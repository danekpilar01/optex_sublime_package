import sublime
import sublime_plugin


class CompletionListener(sublime_plugin.EventListener):



	"""
	As the eventListener is initialized, we need to load the TeX primitives and OpTeX macros
	and save them as member variables
	"""
	def on_init(self,views):

		

		try:
			"""
			We need to use the find_resource method because current working directory
			has different path than the Packgages directory and is platform dependent
			
			load_resource method reads the file, but the parameter is not standard path
			but the format that is returned by find_resource method
			"""

			primitives_find_result = sublime.find_resources("tex_primitives.txt")[0]
			self.primitives = set(sublime.load_resource(primitives_find_result).split('\n'))


			optex_macros_find_result = sublime.find_resources("optex_macros.txt")[0]
			self.optex_macros = set(sublime.load_resource(optex_macros_find_result).split('\n'))


			math_control_find_result = sublime.find_resources("math_control_sequences.txt")[0]
			self.math_control = set(sublime.load_resource(math_control_find_result).split('\n'))


		except:
			sublime.message_dialog("Error while reading the TeX primitives and OpTeX macros.")


		self.user_macros = set()

	#is triggered everytime a completion can be shown to user
	def on_query_completions(self, view, prefix, locations):
		
		#first we have to check the context
		#this completion listener should react only to optex source files


		if not view.match_selector(locations[0], "source.optex") or len(prefix) == 0:
			return []

		#ignore case when suggesting completions
		prefix = prefix.lower()

		output = list()
		



		#check if a blackslash is before prefix
		added_prefix = "\\"

		pt = locations[0]-2

		if pt >= 0 and view.substr(pt) == '\\':
			added_prefix = ""
		

		#look in TeX primitives
		for val in self.primitives:
			if val.lower().startswith(prefix):
				output.append([val+" - TeX primitive",added_prefix+val])

		#look in OpTeX macros
		for val in self.optex_macros:
			if val.lower().startswith(prefix):
				output.append([val+" - OpTeX macro",added_prefix+val])

		#look in user-defined macros
		for val in self.user_macros:
			if val.lower().startswith(prefix):
				output.append([val+" - user-defined macro",added_prefix+val])

		#if in math context, look in math control sequences
		if(view.match_selector(locations[0], "text.math") or view.match_selector(locations[0], "storage.math")):
			for val in self.math_control:
				if val.lower().startswith(prefix):
					output.append([val+" - math control sequence",added_prefix+val])



		#return output
		#turns off the autocompletion based on what user already typed
		return sublime.CompletionList(output,sublime.INHIBIT_WORD_COMPLETIONS)



	def on_modified(self, view):

		result = view.find_by_selector("entity.name.user_macro.optex")

		for res in result:
			res = view.substr(res)[1:]
			if res not in self.user_macros:
				self.user_macros.add(res)