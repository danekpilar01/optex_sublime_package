import sublime
import sublime_plugin


class CompletionListener(sublime_plugin.EventListener):



	#is triggered everytime a completion can be shown to user
	def on_query_compleltions(self, view, prefix, locations):
		
		#first we have to check the context
		#this completion listener should react only on optex srouce files
		if not view.match_selector(locations[0], "source.optex")
			return []