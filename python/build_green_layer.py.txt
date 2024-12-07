import cv2
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Wait for the connection to establish

# Function to send commands to Arduino
def send_motor_command(motor_id, action):
    """
    motor_id: Motor number ( 1 for arm up/down, 2 for gripper, 3 for base rotation)
    action: FORWARD, BACKWARD, or RELEASE
    """
    command = f"{motor_id}:{action}\n"
    arduino.write(command.encode())
    time.sleep(0.05)  # Short delay to avoid command overlap

# Open Camera 1 for cube and hand detection
camera = cv2.VideoCapture(1)  # Explicitly using Camera 1
if not camera.isOpened():
    print("Error: Could not access Camera 1.")
    exit()

try:
    for cubeidx in range(3):  # Build three blocks for the green layer
        delaybackwards = 0.6
        delayforwards = 1.4
        cube_detected = False

        # Step 1: Detect the green cube
        while not cube_detected:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab a frame.")
                break

            # Resize frame for faster processing 
            frame = cv2.resize(frame, (640, 480))

            # Convert the frame to HSV for green cube detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define color range for green
            lower_green = (35, 100, 100)
            upper_green = (85, 255, 255)

            # Create a mask for green
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # Apply morphological operations to reduce noise
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Check if the cube is detected
            if cv2.countNonZero(mask) > 500:  # Adjust threshold for detection
                print("Green cube detected!")
                cube_detected = True

                send_motor_command(1, "RELEASE")  # Stop Motor 1 (arm down)

                # Close the gripper to hold the cube
                print("Closing gripper to hold the cube.")
                send_motor_command(2, "FORWARD")  # Close gripper
                time.sleep(3)
                send_motor_command(2, "RELEASE")

                # Lift the cube slightly
                print("Lifting the cube.")
                send_motor_command(1, "BACKWARD")  # Move arm up
                time.sleep(5)
                send_motor_command(1, "RELEASE")
            else:
                print("Searching for cube...")
                send_motor_command(1, "FORWARD")  # Move Motor 1 (arm down)

            # Show the camera feed and mask for debugging
            cv2.imshow("Camera Feed", frame)
            cv2.imshow("Green Mask", mask)

        # Step 2: Rotate base
        send_motor_command(3, "FORWARD")
        time.sleep(5.7 + cubeidx * delayforwards)
        send_motor_command(3, "RELEASE")

        # Step 3: Place cube
        print("Placing the cube.")
        send_motor_command(1, "FORWARD")
        time.sleep(2)
        send_motor_command(1, "RELEASE")

        print("Opening gripper.")
        send_motor_command(2, "BACKWARD")
        time.sleep(2)
        send_motor_command(2, "RELEASE")

        print("Lifting arm back up.")
        send_motor_command(1, "BACKWARD")
        time.sleep(3)
        send_motor_command(1, "RELEASE")

        print("Returning base to position.")
        send_motor_command(3, "BACKWARD")
        time.sleep(5.4 + delaybackwards * cubeidx * 0.5)
        send_motor_command(3, "RELEASE")

finally:
    send_motor_command(1, "RELEASE")
    send_motor_command(2, "RELEASE")
    send_motor_command(3, "RELEASE")
    camera.release()
    cv2.destroyAllWindows()
    arduino.close()
