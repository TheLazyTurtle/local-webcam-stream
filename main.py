from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Capture video stream from the webcam
video_capture = None
for x in range(0, 10):
	video_capture = cv2.VideoCapture(x)

	if (video_capture.getBackendName() != "DSHOW"):
		continue

	video_capture.set(3, 1920) # Width
	video_capture.set(4, 1080) # Height
	print(video_capture.getBackendName())
	break

def generate_frames():
    while True:
        # Read frame from the webcam
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Serve the frame as part of an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    # Return the HTML page that shows the webcam stream
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Serve the video feed as a multipart response
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	if (video_capture == None):
		raise Exception("Could not find camera to connect")
	app.run(host='0.0.0.0', port=5000)
