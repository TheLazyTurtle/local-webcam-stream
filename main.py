from video import VideoController
from obs import ObsController

from flask import Flask, render_template, Response, jsonify, request
import cv2

app = Flask(__name__)
video_controller = VideoController()
obs_controller = ObsController()
obs_controller.connect()

def generate_frames():
    while True:
        # Read frame from the webcam
        success, frame = video_controller.video_capture.read()
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

@app.route('/switch_scene')
def switch_scene():
    scene_name = request.args.get("scene_name")
    obs_controller.switch_to_scene(scene_name)
    return jsonify({'success': True})

@app.route('/get_scenes')
def get_scenes():
    scenes = obs_controller.get_scenes()
    result = []
    for s in scenes:
        result.append({"name": obs_controller.get_name_of_scene(s)})
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
