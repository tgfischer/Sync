import sublime, sublime_plugin, socket
from threading import Thread

class SyncCommand(sublime_plugin.TextCommand):
	def server(self):
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('localhost', 8089))
		serversocket.listen(5) # become a server socket, maximum 5 connections

		print("Server started")

		while True:
			connection, address = serversocket.accept()
			buf = connection.recv(64)

			if len(buf) > 0:
				allcontent = sublime.Region(0, self.view.size())
				self.view.replace(edit, allcontent, message)
				
	def run(self, edit):
		thread = Thread(target = self.server, args = ())
		thread.start()