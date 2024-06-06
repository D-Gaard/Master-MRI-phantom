#include <Stepper.h>

// Define number of steps per revolution for your stepper motors
const int stepsPerRevolution = 200; // Change this according to your motor's specification

// Define the motor pins
const int stepPin = 2;
const int dirPin = 3;

// Create stepper object
Stepper stepper(stepsPerRevolution, stepPin, dirPin);

void setup() {
  // Set the motor pins as outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read serial command
    if (command.startsWith("turnon")) {
      stepper.setSpeed(100); // Set the speed (adjust as needed)
      stepper.step(1);      // Step one step
    } else if (command.startsWith("turndirection")) {
      // Toggle direction
      digitalWrite(dirPin, !digitalRead(dirPin));
    }
  }
}