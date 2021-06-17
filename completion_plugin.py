import sublime
import sublime_plugin


class CompletionListener(sublime_plugin.EventListener):

	"""
	As the eventListener is initialized, we need to load the TeX primitives and OpTeX macros
	and save them as member vaiables
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
			self.primitives = sublime.load_resource(primitives_find_result).split('\n')


			optex_macros_find_result = sublime.find_resources("optex_macros.txt")[0]
			self.optex_macros = sublime.load_resource(optex_macros_find_result).split('\n')

		except:
			sublime.message_dialog("Error while reading the TeX primitives and OpTeX macros.")




	#is triggered everytime a completion can be shown to user
	def on_query_completions(self, view, prefix, locations):
		
		#first we have to check the context
		#this completion listener should react only on optex srouce files
		if not view.match_selector(locations[0], "source.optex"):
			return []

		return [["nevim", "ajsldfjsaldfja;sdfj;"]]