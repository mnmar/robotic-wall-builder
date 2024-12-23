import cv2
import matplotlib.pyplot as plt
import time
from IPython.display import clear_output

# Open the camera
camera = cv2.VideoCapture(1) 

if not camera.isOpened():
    print("Error: Could not access the camera.")
    camera.release()
    exit()

print("Camera feed will display for 60 seconds.")

# Set the timeout duration (in seconds)
timeout_duration = 60
start_time = time.time()  # Record the start time

try:
    while True:
        ret, frame = camera.read()  # Capture a frame
        if not ret:
            print("Failed to grab a frame.")
            break

        # Convert the frame to RGB (matplotlib expects RGB format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Use matplotlib to display the frame
        clear_output(wait=True) 
        plt.figure(figsize=(5, 2)) 
        plt.imshow(frame_rgb)
        plt.axis('off')  # Hide axes
        plt.show()

        # Exit the loop after the timeout duration
        if time.time() - start_time > timeout_duration:
            print("Time's up! Exiting the camera feed.")
            break

except KeyboardInterrupt:
    print("Camera feed interrupted by user.")

# Release the camera
camera.release()
