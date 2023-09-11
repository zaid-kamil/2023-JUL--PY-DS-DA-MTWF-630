import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import cv2

path = 'computer_vision/gesture_recognizer.task'

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

results = []
# Create a gesture recognizer instance with the live stream mode:
def process_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    results.append(result)

options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=process_result)
with GestureRecognizer.create_from_options(options) as recognizer:
    print("Gesture recognizer model loaded.")
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        state, image = cam.read()
        if not state: break
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        ts = int(time.time() * 1000)
        recognizer.recognize_async(mp_image, ts)
        # Draw the hand annotations on the image.
        h,w,_ = image.shape
        cv2.rectangle(image, (0, h-80), (w, h), (0,0,0), -1)
        if results:
            result = results.pop()
            gesture, hand = "", ""
            # Get the first gesture and hand info.
            if len(result.gestures) > 0:
                gesture = result.gestures[0][0].category_name
                hand = result.handedness[0][0].category_name
                cv2.putText(image, f"{hand} - {gesture}",
                    (40,h-40), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 255), 1)
            # Draw the hand landmarks on the image.
            for landmark in result.hand_landmarks:
                for i in landmark:
                    nx, ny= i.x, i.y
                    x, y = int(nx*w), int(ny*h) # normalized to pixel size
                    print('index finger at', x, y)
                    cv2.circle(image, (x,y), 5, (0,255,0), -1)
        cv2.imshow('MediaPipe Gesture Recognition', image)
        key = cv2.waitKey(10)
        if key == 27: break
    cam.release()
    cv2.destroyAllWindows()

