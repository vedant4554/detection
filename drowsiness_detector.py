import cv2
import dlib
import pyttsx3
import numpy as np
from scipy.spatial import distance
import threading
import time

class DrowsinessDetector:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        
        # Face detection and landmark prediction
        self.face_detector = dlib.get_frontal_face_detector()
        
        # Try to load the shape predictor
        try:
            self.dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        except Exception as e:
            print("Error: Could not load shape_predictor_68_face_landmarks.dat")
            print("Please download it from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
            print("Extract and place it in the same directory as this script.")
            return
        
        # Drowsiness detection parameters
        self.EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold
        self.EYE_AR_CONSEC_FRAMES = 20  # Consecutive frames for drowsiness
        self.COUNTER = 0
        self.ALARM_ON = False
        
        # Eye landmark points (based on 68-point facial landmark detector)
        self.LEFT_EYE_POINTS = list(range(36, 42))
        self.RIGHT_EYE_POINTS = list(range(42, 48))
        
    def calculate_eye_aspect_ratio(self, eye_points):
        """Calculate the eye aspect ratio using euclidean distances"""
        # Vertical eye landmarks
        A = distance.euclidean(eye_points[1], eye_points[5])
        B = distance.euclidean(eye_points[2], eye_points[4])
        
        # Horizontal eye landmark
        C = distance.euclidean(eye_points[0], eye_points[3])
        
        # Eye aspect ratio
        ear = (A + B) / (2.0 * C)
        return ear
    
    def sound_alarm(self):
        """Play alarm sound using text-to-speech"""
        if not self.ALARM_ON:
            self.ALARM_ON = True
            self.engine.say("Wake up! You seem to be drowsy!")
            self.engine.runAndWait()
            self.ALARM_ON = False
    
    def draw_eye_landmarks(self, frame, eye_points):
        """Draw eye landmarks on the frame"""
        for i in range(len(eye_points)):
            cv2.circle(frame, eye_points[i], 2, (0, 255, 0), -1)
        
        # Draw eye contour
        eye_hull = cv2.convexHull(np.array(eye_points))
        cv2.drawContours(frame, [eye_hull], -1, (0, 255, 0), 1)
    
    def detect_drowsiness(self):
        """Main drowsiness detection loop"""
        print("Starting drowsiness detection...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Resize frame for faster processing
            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_detector(gray)
            
            for face in faces:
                # Get facial landmarks
                landmarks = self.dlib_facelandmark(gray, face)
                
                # Extract eye coordinates
                left_eye = []
                right_eye = []
                
                for n in self.LEFT_EYE_POINTS:
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    left_eye.append((x, y))
                
                for n in self.RIGHT_EYE_POINTS:
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    right_eye.append((x, y))
                
                # Calculate eye aspect ratios
                left_ear = self.calculate_eye_aspect_ratio(left_eye)
                right_ear = self.calculate_eye_aspect_ratio(right_eye)
                
                # Average eye aspect ratio
                ear = (left_ear + right_ear) / 2.0
                
                # Draw eye landmarks
                self.draw_eye_landmarks(frame, left_eye)
                self.draw_eye_landmarks(frame, right_eye)
                
                # Check for drowsiness
                if ear < self.EYE_AR_THRESH:
                    self.COUNTER += 1
                    
                    # If eyes closed for sufficient consecutive frames
                    if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                        # Sound alarm in separate thread to avoid blocking
                        if not self.ALARM_ON:
                            alarm_thread = threading.Thread(target=self.sound_alarm)
                            alarm_thread.daemon = True
                            alarm_thread.start()
                        
                        # Draw alert on frame
                        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    self.COUNTER = 0
                
                # Display eye aspect ratio and counter
                cv2.putText(frame, f"EAR: {ear:.3f}", (480, 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Counter: {self.COUNTER}", (480, 60),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Draw face rectangle
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Display frame
            cv2.imshow("Drowsiness Detection", frame)
            
            # Break loop on 'q' key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        # Clean up
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    detector = DrowsinessDetector()
    detector.detect_drowsiness()

if __name__ == "__main__":
    main() 