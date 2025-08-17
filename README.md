# Drowsiness Detection System

A real-time drowsiness detection system using OpenCV and facial landmark detection. This project can detect when a person is getting drowsy by monitoring their eye aspect ratio and trigger audio alerts to prevent accidents.

## Features

- **Real-time face detection** using dlib's face detector
- **Eye landmark detection** with 68-point facial landmark predictor
- **Eye Aspect Ratio (EAR) calculation** to determine if eyes are closed
- **Audio alerts** using text-to-speech when drowsiness is detected
- **Visual indicators** showing eye landmarks and drowsiness status
- **Configurable sensitivity** for drowsiness detection

## How It Works

The system works by:

1. **Face Detection**: Detects faces in the video stream
2. **Landmark Detection**: Identifies 68 facial landmarks, focusing on eye regions
3. **EAR Calculation**: Calculates Eye Aspect Ratio using euclidean distances
4. **Drowsiness Detection**: Monitors if EAR falls below threshold for consecutive frames
5. **Alert System**: Triggers audio and visual alerts when drowsiness is detected

## Installation

### Option 1: Automatic Setup (Recommended)

Run the setup script to install all dependencies automatically:

```bash
python setup.py
```

### Option 2: Manual Setup

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download facial landmarks file:**
   ```bash
   python download_landmarks.py
   ```

## Usage

1. **Run the drowsiness detector:**
   ```bash
   python drowsiness_detector.py
   ```

2. **Position yourself in front of the camera**
   - Make sure your face is clearly visible
   - Ensure good lighting conditions

3. **The system will:**
   - Display your video feed with eye landmarks
   - Show Eye Aspect Ratio (EAR) value
   - Count consecutive frames with closed eyes
   - Trigger "DROWSINESS ALERT!" when sleepiness is detected

4. **Press 'q' to quit the application**

## Configuration

You can adjust the sensitivity by modifying these parameters in `drowsiness_detector.py`:

```python
self.EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold (lower = more sensitive)
self.EYE_AR_CONSEC_FRAMES = 20  # Consecutive frames before alert (lower = faster alert)
```

## Requirements

- Python 3.7+
- Webcam/Camera
- Operating System: Windows, macOS, or Linux

## Dependencies

- opencv-python (4.8.1.78)
- dlib (19.24.2)
- scipy (1.11.4)
- pyttsx3 (2.90)
- numpy (1.24.3)
- imutils (0.5.4)
- cmake (3.27.7)

## Troubleshooting

### Common Issues:

1. **"Could not load shape_predictor_68_face_landmarks.dat"**
   - Run: `python download_landmarks.py`
   - Ensure you have internet connection

2. **Camera not working:**
   - Check if camera is being used by another application
   - Try changing camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

3. **dlib installation issues:**
   - Install cmake first: `pip install cmake`
   - On Windows: Install Visual Studio Build Tools
   - On macOS: Install Xcode command line tools
   - On Linux: Install build-essential

4. **No face detected:**
   - Ensure good lighting
   - Position face clearly in camera view
   - Try adjusting camera angle

## Technical Details

### Eye Aspect Ratio (EAR) Formula:

```
EAR = (|p2 - p6| + |p3 - p5|) / (2 * |p1 - p4|)
```

Where p1, p2, p3, p4, p5, p6 are the eye landmark points.

### Eye Landmark Points:
- **Left Eye**: Points 36-41 (0-indexed)
- **Right Eye**: Points 42-47 (0-indexed)

## Applications

- **Driver monitoring systems**
- **Workplace safety monitoring**
- **Student attention monitoring**
- **Medical patient monitoring**
- **Security surveillance enhancement**

## Future Enhancements

- [ ] Add head pose estimation
- [ ] Implement yawning detection
- [ ] Add mobile app version
- [ ] Include multiple alert types (sound, vibration, email)
- [ ] Add data logging and analytics
- [ ] Implement machine learning-based improvements

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is based on the tutorial from [GeeksforGeeks](https://www.geeksforgeeks.org/python/python-opencv-drowsiness-detection/) and is intended for educational and safety purposes.

## Acknowledgments

- **dlib library** for facial landmark detection
- **OpenCV** for computer vision capabilities
- **GeeksforGeeks** for the original tutorial inspiration
- **Shape predictor model** trained by dlib team 