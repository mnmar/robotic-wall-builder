#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

// Create the motor objects
Adafruit_DCMotor *motor1 = AFMS.getMotor(2); // Arm up/down
Adafruit_DCMotor *motor2 = AFMS.getMotor(1); // Gripper open/close
Adafruit_DCMotor *motor3 = AFMS.getMotor(4); // Base rotation

void setup() {
  Serial.begin(9600);  // Start serial communication
  AFMS.begin();        // Initialize the shield

  // Set motor speeds
  motor1->setSpeed(100);  // Arm up/down
  motor2->setSpeed(80);   // Gripper open/close
  motor3->setSpeed(90);   // Base rotation
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    int motor_id = command.substring(0, command.indexOf(':')).toInt();
    String action = command.substring(command.indexOf(':') + 1);

    if (motor_id == 1) { // Control Motor 1 (arm up/down)
      if (action == "FORWARD") {
        motor1->run(FORWARD);  // Arm moves down
      } else if (action == "BACKWARD") {
        motor1->run(BACKWARD);  // Arm moves up
      } else if (action == "RELEASE") {
        motor1->run(RELEASE);  // Stop motor
      }
    } else if (motor_id == 2) { // Control Motor 2 (gripper)
      if (action == "FORWARD") {
        motor2->run(FORWARD);  // Close gripper
      } else if (action == "BACKWARD") {
        motor2->run(BACKWARD);  // Open gripper
      } else if (action == "RELEASE") {
        motor2->run(RELEASE);  // Stop motor
      }
    } else if (motor_id == 3) { // Control Motor 3 (base rotation)
      if (action == "FORWARD") {
        motor3->run(FORWARD);  // Rotate base clockwise
      } else if (action == "BACKWARD") {
        motor3->run(BACKWARD);  // Rotate base counter-clockwise
      } else if (action == "RELEASE") {
        motor3->run(RELEASE);  // Stop motor
      }
    }
  }
}
