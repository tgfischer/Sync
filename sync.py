import sublime, sublime_plugin, socket, threading, time
from threading import Thread

PORT = 3003
TIMEOUT = 5

class SyncCommand(sublime_plugin.TextCommand):		
	def run(self, edit):
		# thread = ServerThread(edit, self.view, TIMEOUT)
		thread = ClientThread(self.view, TIMEOUT)

		thread.start()


class ServerThread(threading.Thread):
	def __init__(self, edit, view, timeout):
		self.edit = edit
		self.view = view
		self.timeout = timeout

		threading.Thread.__init__(self)

	def run(self):
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('localhost', PORT))
		serversocket.listen(5) # become a server socket, maximum 5 connections

		print("Server started")

		while True:
			connection, address = serversocket.accept()
			self.text = connection.recv(1024)

			if len(self.text) > 0:
				sublime.set_timeout(self.callback, 1)

	def callback(self):
		region = sublime.Region(0, self.view.size())
		self.view.replace(self.edit, region, self.text)


class ClientThread(threading.Thread):
	def __init__(self, view, timeout):
		self.view = view
		self.timeout = timeout

		threading.Thread.__init__(self)

	def run(self):
		print("Client started. Looking for a server...")

		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect(('localhost', PORT))

		print("Connected!")

		while True:
			region = sublime.Region(0, self.view.size())
			clientsocket.send(bytes(str(self.view.substr(region)), 'UTF-8'))
			time.sleep(1)