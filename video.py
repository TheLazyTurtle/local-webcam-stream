import cv2

class VideoController:
	def __init__(self, max_camera_search_range = 10):
		self.video_capture = None

		for c in range(0, max_camera_search_range):
			self.video_capture = cv2.VideoCapture(c)

			if (self.video_capture.getBackendName() != "DSHOW"):
				continue

			self.video_capture.set(3, 1920) # Width
			self.video_capture.set(4, 1080) # Height
			break
		pass
