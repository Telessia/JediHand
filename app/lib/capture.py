from jinja2 import Undefined
import mediapipe as mp
import cv2
import lib.styles.styles as styles

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
counter = 0 #count the frame before performing an action
cache = 0

def stream():
  cache = 0
  # For webcam input:
  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.7,
      min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              styles.get_default_hand_landmarks_style(),
              styles.get_default_hand_connections_style())
      # Flip the image horizontally for a selfie-view display.
      image = cv2.flip(image, 1)
      image_height, image_width, _ = image.shape
      textcoord = (image_width - 200, image_height - 60)
      ret, buffer = cv2.imencode('.jpg', image)
      image = buffer.tobytes()
      yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')  # concat frame one by one and show result
        
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()
  
def shot():
  # For webcam input:
  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.7,
      min_tracking_confidence=0.7) as hands:
      success, image = cap.read()
      cap.release()
      original_image = image
      

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              styles.get_default_hand_landmarks_style(),
              styles.get_default_hand_connections_style())
      # Flip the image horizontally for a selfie-view display.
      no_flip_with_marks = image
      image = cv2.flip(image, 1)
      # Cropping an image
      ret, buffer = cv2.imencode('.jpg', image)
      path_original = "app/static/tmp/lastest.jpg"
      path = "app/static/tmp/lastest_with_marks.jpg"
      if results.multi_hand_landmarks:
        cv2.imwrite(path_original,original_image)
        cv2.imwrite(path,no_flip_with_marks)
        return path_original,path,results.multi_hand_landmarks[0].landmark
      else:
        cv2.imwrite(path_original,original_image)
        cv2.imwrite(path,no_flip_with_marks)
        return path_original,path,None


      