import time
import os
from obswebsocket import obsws, requests, events

class ObsController:
	def __init__(self):
		self.host = "localhost"  # Host IP where OBS is running
		self.port = 4455         # Default OBS WebSocket port
		self.password = os.environ["OBS_WEBSOCKET_PASS"]  # Password if set in OBS WebSocket settings

	def on_event(message):
		print("Got message: {}".format(message))

	def on_switch(message):
		print("You changed the scene to {}".format(message.getSceneName()))

	def connect(self):
		try:
			self.ws = obsws(self.host, self.port, self.password)
			# Optional debug callbacks
			# self.ws.register(self.on_event)
			# self.ws.register(self.on_switch, events.SwitchScenes)
			# self.ws.register(self.on_switch, events.CurrentProgramSceneChanged)
			self.ws.connect()
		except Exception as err:
			print(f"We got an error while trying to make connection: {err}")

	def disconnect(self):
		self.ws.disconnect()

	def get_scenes(self):
		return self.ws.call(requests.GetSceneList()).getScenes()

	def switch_to_scene(self, name):
		self.ws.call(requests.SetCurrentProgramScene(sceneName=name))
		return

	def get_name_of_scene(self, scene):
		return scene['sceneName']