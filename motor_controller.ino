// This is very similar to Example 3 - Receive with start- and end-markers
//    in Serial Input Basics   http://forum.arduino.cc/index.php?topic=396450.0
#include <AccelStepper.h>

//globals for data transfer
const byte numChars = 64; //by default uno only has 32 bytes avaliable,
char receivedChars[numChars];
boolean newData = false;

//globals for motor controll
const int stepsPerRevolution = 200; //1.8 deg per step
const float maximalAcceleration = 150.0;

const int dirPin1 = 2;
const int dirPin2 = 4;
const int dirPin3 = 6;
const int dirPin4 = 8;
const int dirPin5 = 10;
const int dirPin6 = 12;

const int stepPin1 = 3;
const int stepPin2 = 5;
const int stepPin3 = 7;
const int stepPin4 = 9;
const int stepPin5 = 11;
const int stepPin6 = 13;



AccelStepper S1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper S2(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper S3(AccelStepper::DRIVER, stepPin3, dirPin3);
AccelStepper S4(AccelStepper::DRIVER, stepPin4, dirPin4);
AccelStepper S5(AccelStepper::DRIVER, stepPin5, dirPin5);
AccelStepper S6(AccelStepper::DRIVER, stepPin6, dirPin6);

//setup motors and serial port
void setup() {
    Serial.begin(1000000); //set serial port

    //setup motors
    S1.setMaxSpeed(stepsPerRevolution*10);
    S1.setAcceleration(maximalAcceleration);
    S2.setMaxSpeed(stepsPerRevolution*10);
    S2.setAcceleration(maximalAcceleration);
    S3.setMaxSpeed(stepsPerRevolution*10);
    S3.setAcceleration(maximalAcceleration);
    S4.setMaxSpeed(stepsPerRevolution*10);
    S4.setAcceleration(maximalAcceleration);
    S5.setMaxSpeed(stepsPerRevolution*10);
    S5.setAcceleration(maximalAcceleration);
    S6.setMaxSpeed(stepsPerRevolution*10);
    S6.setAcceleration(maximalAcceleration);

    //let the pc know that setup has been completed
    Serial.println("<Arduino is ready>");
}


//main recive/process loop
void loop() {
    recvWithStartEndMarkers();
    replyToPython();
}

//recive msg "<...>"
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//process msg from host computer and run motors acrordingly
void replyToPython() {
    if (newData == true) {

        char firstChar;
        long motorSteps[6];
        unsigned long runtime;
        parseReceivedString(receivedChars, firstChar, motorSteps, runtime);

        Serial.print("<This just in ... ");
        Serial.print(receivedChars);
        Serial.print("   ");
        Serial.print(firstChar);

        for (int i = 0; i<6; i++){
          Serial.print("   ");
          Serial.print(motorSteps[i]);
        }
        Serial.print("   ");
        Serial.print(runtime);
        Serial.print("   ");
        Serial.print(millis());
        Serial.print('>');
  
        driveMotors(motorSteps,runtime);
        newData = false; //signal that the next message can be read
    }
}

//parse the motor string (format described in motor_ui.ipynb/report)
void parseReceivedString(char* receivedString, char& firstChar, long numbers[], unsigned long& value) {
  // Extract the first character
  firstChar = receivedString[0];

  Serial.print("<");
  Serial.print("first: ");
  Serial.print(firstChar);
  Serial.print(">");

  if (firstChar == '<'){ //failsafe incase of buffer overflow causing wrong values
    Serial.print("<ENCOUNTERD OVERFLOW ... DELAY 999999>");
    delay(999999);
  }

  // Extract 6 numbers (each stored as 4 hex characters)
  for (int i = 0; i < 6; i++) {
    char hexString[5];
    strncpy(hexString, &receivedString[1 + i * 4], 4); // Copy each 4-character hex string
    hexString[4] = '\0'; // Null-terminate the string
    long num = strtol(hexString, NULL, 16); // Convert hex string to long integer

    // Handle negative numbers
    if (num & 0x8000) { // Check if the most significant bit is set
      num |= 0xFFFF0000; // Set all bits above the 16th position
    }
    
    numbers[i] = num;
  }

  // Extract the last 4-character hex string
  char hexValue[5];
  strncpy(hexValue, &receivedString[25], 4);
  hexValue[4] = '\0';
  value = strtol(hexValue, NULL, 16);
}

//drive the motors in the specified amount of time
void driveMotors(long motorsteps[],unsigned long runtime){
  S1.move(motorsteps[0]);
  S2.move(motorsteps[1]);
  S3.move(motorsteps[2]);
  S4.move(motorsteps[3]);
  S5.move(motorsteps[4]);
  S6.move(motorsteps[5]);

  Serial.print("<Start driving");
  Serial.print(millis());
  Serial.println(">");
  unsigned long curTime = millis();
  while (curTime + runtime > millis()){
    S1.run();
    S2.run();
    S3.run();
    S4.run();
    S5.run();
    S6.run();
  }
  Serial.print("<Finished driving ");
  Serial.print(millis());
  if (!S1.isRunning()){
    Serial.print(" S1done");
  }
  if (!S2.isRunning()){
    Serial.print(" S2done");
  }
  if (!S3.isRunning()){
    Serial.print(" S3done");
  }
  if (!S4.isRunning()){
    Serial.print(" S4done");
  }
  if (!S5.isRunning()){
    Serial.print(" S5done");
  }
  if (!S6.isRunning()){
    Serial.print(" S6done");
  }
  Serial.println(">");
}
