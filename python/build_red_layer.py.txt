import cv2
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600) 
time.sleep(2)  # Wait for the connection to establish

# Function to send commands to Arduino
def send_motor_command(motor_id, action):
    """
    motor_id: Motor number (1 for arm up/down, 2 for gripper, 3 for base rotation)
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
#######################################################################1st################################################################
        delaybackwards=0.6
        delayforwards=1.4
        cube_detected = False
        # Step 1: Detect the red cube
        while not cube_detected:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab a frame.")
                break
            # Resize frame for faster processing (optional)
            frame = cv2.resize(frame, (640, 480))
            # Convert the frame to HSV for red cube detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Define color range for red (red has two ranges due to hue wraparound)
            lower_red1 = (0, 120, 70)
            upper_red1 = (10, 255, 255)
            lower_red2 = (170, 120, 70)
            upper_red2 = (180, 255, 255)
            # Create masks for both red ranges
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            # Combine both masks
            mask = cv2.bitwise_or(mask1, mask2)
            # Apply morphological operations to reduce noise
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Check if the cube is detected
            if cv2.countNonZero(mask) > 500:  # Adjust threshold for detection
                print("Cube detected!")
                cube_detected = True
                send_motor_command(1, "RELEASE")  # Stop Motor 1 (arm down)
    
                # Close the gripper to hold the cube
                print("Closing gripper to hold the cube.")
                send_motor_command(2, "FORWARD")  # Close gripper
                time.sleep(3)  # Wait for the gripper to fully close
                send_motor_command(2, "RELEASE")  # Stop Motor 2
    
                # Lift the cube slightly
                print("Lifting the cube.")
                send_motor_command(1, "BACKWARD")  # Move arm up
                time.sleep(5)  # Adjust time for lifting
                send_motor_command(1, "RELEASE")  # Stop Motor 1
            else:
                print("Searching for cube...")
                send_motor_command(1, "FORWARD")  # Move Motor 1 (arm down)
    
            # Show the camera feed and mask for debugging
            cv2.imshow("Camera Feed", frame)
            cv2.imshow("Red Mask", mask)

        # Step 2: Rotate base
        send_motor_command(3, "FORWARD")  # rotate
        time.sleep(5.7 )  
        send_motor_command(3, "RELEASE")  # Stop Motor 3
    
        # Step 3: Move arm down and release cube
        print("Moving arm down to place the cube.")
        send_motor_command(1, "FORWARD")  # Lower the arm
        time.sleep(2)  # Adjust time for lowering
        send_motor_command(1, "RELEASE")  # Stop Motor 1

        print("Opening gripper to release the cube.")
        send_motor_command(2, "BACKWARD")  # Open the gripper
        time.sleep(2)  # Adjust time to open gripper
        send_motor_command(2, "RELEASE")  # Stop Motor 2
    
        print("Lifting arm back up.")
        send_motor_command(1, "BACKWARD")  # Lift the arm back up
        time.sleep(3)  # Adjust time for lifting
        send_motor_command(1, "RELEASE")  # Stop Motor 1
        
        # Rotate the base back to its original position
        print("Rotating base back to the original position.")
        send_motor_command(3, "BACKWARD")  # Rotate base forward to return
        time.sleep(5.5)  # Adjust time based on how far it needs to rotate back
        send_motor_command(3, "RELEASE")  # Stop Motor 3
#######################################################################2nd################################################################
        cube_detected = False
        # Step 1: Detect the red cube
        while not cube_detected:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab a frame.")
                break
            # Resize frame for faster processing 
            frame = cv2.resize(frame, (640, 480))
            # Convert the frame to HSV for red cube detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Define color range for red (red has two ranges due to hue wraparound)
            lower_red1 = (0, 120, 70)
            upper_red1 = (10, 255, 255)
            lower_red2 = (170, 120, 70)
            upper_red2 = (180, 255, 255)
            # Create masks for both red ranges
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            # Combine both masks
            mask = cv2.bitwise_or(mask1, mask2)
            # Apply morphological operations to reduce noise
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Check if the cube is detected
            if cv2.countNonZero(mask) > 500:  # Adjust threshold for detection
                print("Cube detected!")
                cube_detected = True
                send_motor_command(1, "RELEASE")  # Stop Motor 1 (arm down)
    
                # Close the gripper to hold the cube
                print("Closing gripper to hold the cube.")
                send_motor_command(2, "FORWARD")  # Close gripper
                time.sleep(3)  # Wait for the gripper to fully close
                send_motor_command(2, "RELEASE")  # Stop Motor 2
    
                # Lift the cube slightly
                print("Lifting the cube.")
                send_motor_command(1, "BACKWARD")  # Move arm up
                time.sleep(5)  # Adjust time for lifting
                send_motor_command(1, "RELEASE")  # Stop Motor 1
            else:
                print("Searching for cube...")
                send_motor_command(1, "FORWARD")  # Move Motor 1 (arm down)
    
            # Show the camera feed and mask for debugging
            cv2.imshow("Camera Feed", frame)
            cv2.imshow("Red Mask", mask)

        # Step 2: Rotate base
        send_motor_command(3, "FORWARD")  # rotate
        time.sleep(5.7 + 1.4)  
        send_motor_command(3, "RELEASE")  # Stop Motor 3
    
        # Step 3: Move arm down and release cube
        print("Moving arm down to place the cube.")
        send_motor_command(1, "FORWARD")  # Lower the arm
        time.sleep(1.3)  # Adjust time for lowering
        send_motor_command(1, "RELEASE")  # Stop Motor 1

        print("Opening gripper to release the cube.")
        send_motor_command(2, "BACKWARD")  # Open the gripper
        time.sleep(2)  # Adjust time to open gripper
        send_motor_command(2, "RELEASE")  # Stop Motor 2
    
        print("Lifting arm back up.")
        send_motor_command(1, "BACKWARD")  # Lift the arm back up
        time.sleep(3)  # Adjust time for lifting
        send_motor_command(1, "RELEASE")  # Stop Motor 1
        
        # Rotate the base back to its original position
        print("Rotating base back to the original position.")
        send_motor_command(3, "BACKWARD")  # Rotate base forward to return
        time.sleep(5.4+1*0.8)  # Adjust time based on how far it needs to rotate back
        send_motor_command(3, "RELEASE")  # Stop Motor 3
#######################################################################3rd################################################################
        cube_detected = False
        # Step 1: Detect the red cube
        while not cube_detected:
            ret, frame = camera.read()
            if not ret:
                print("Failed to grab a frame.")
                break
            # Resize frame for faster processing (optional)
            frame = cv2.resize(frame, (640, 480))
            # Convert the frame to HSV for red cube detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Define color range for red (red has two ranges due to hue wraparound)
            lower_red1 = (0, 120, 70)
            upper_red1 = (10, 255, 255)
            lower_red2 = (170, 120, 70)
            upper_red2 = (180, 255, 255)
            # Create masks for both red ranges
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            # Combine both masks
            mask = cv2.bitwise_or(mask1, mask2)
            # Apply morphological operations to reduce noise
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Check if the cube is detected
            if cv2.countNonZero(mask) > 500:  # Adjust threshold for detection
                print("Cube detected!")
                cube_detected = True
                send_motor_command(1, "RELEASE")  # Stop Motor 1 (arm down)
    
                # Close the gripper to hold the cube
                print("Closing gripper to hold the cube.")
                send_motor_command(2, "FORWARD")  # Close gripper
                time.sleep(3)  # Wait for the gripper to fully close
                send_motor_command(2, "RELEASE")  # Stop Motor 2
    
                # Lift the cube slightly
                print("Lifting the cube.")
                send_motor_command(1, "BACKWARD")  # Move arm up
                time.sleep(5)  # Adjust time for lifting
                send_motor_command(1, "RELEASE")  # Stop Motor 1
            else:
                print("Searching for cube...")
                send_motor_command(1, "FORWARD")  # Move Motor 1 (arm down)
    
            # Show the camera feed and mask for debugging
            cv2.imshow("Camera Feed", frame)
            cv2.imshow("Red Mask", mask)

        # Step 2: Rotate base
        send_motor_command(3, "FORWARD")  # rotate
        time.sleep(5.7 + 2)  
        send_motor_command(3, "RELEASE")  # Stop Motor 3
    
        # Step 3: Move arm down and release cube
        print("Moving arm down to place the cube.")
        send_motor_command(1, "FORWARD")  # Lower the arm
        time.sleep(1.4)  # Adjust time for lowering
        send_motor_command(1, "RELEASE")  # Stop Motor 1

        print("Opening gripper to release the cube.")
        send_motor_command(2, "BACKWARD")  # Open the gripper
        time.sleep(2)  # Adjust time to open gripper
        send_motor_command(2, "RELEASE")  # Stop Motor 2
    
        print("Lifting arm back up.")
        send_motor_command(1, "BACKWARD")  # Lift the arm back up
        time.sleep(3)  # Adjust time for lifting
        send_motor_command(1, "RELEASE")  # Stop Motor 1
        
        # Rotate the base back to its original position
        print("Rotating base back to the original position.")
        send_motor_command(3, "BACKWARD")  # Rotate base forward to return
        time.sleep(5.4+1*1.2)  # Adjust time based on how far it needs to rotate back
        send_motor_command(3, "RELEASE")  # Stop Motor 3
        

finally:
    send_motor_command(1, "RELEASE")  # Stop Motor 1 as a safety measure
    send_motor_command(2, "RELEASE")  # Stop Motor 2 as a safety measure
    send_motor_command(3, "RELEASE")  # Stop Motor 3 as a safety measure
    camera.release()
    cv2.destroyAllWindows()
    arduino.close()
