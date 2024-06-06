#include <AccelStepper.h> //https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html#a68942c66e78fb7f7b5f0cdade6eb7f06

char c = '1';
const int stepsPerRevolution = 200;

const int dirPin1 = 13;
const int dirPin2 = 11;
const int dirPin3 = 9;
const int dirPin4 = 7;
const int dirPin5 = 5;
const int dirPin6 = 3;

const int stepPin1 = 12;
const int stepPin2 = 10;
const int stepPin3 = 8;
const int stepPin4 = 6;
const int stepPin5 = 4;
const int stepPin6 = 2;

AccelStepper S1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper S2(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper S3(AccelStepper::DRIVER, stepPin3, dirPin3);
AccelStepper S4(AccelStepper::DRIVER, stepPin4, dirPin4);
AccelStepper S5(AccelStepper::DRIVER, stepPin5, dirPin5);
AccelStepper S6(AccelStepper::DRIVER, stepPin6, dirPin6);

void setup() {
  pinMode(stepPin1,OUTPUT);
  pinMode(stepPin2,OUTPUT);
  pinMode(stepPin3,OUTPUT);
  pinMode(stepPin4,OUTPUT);
  pinMode(stepPin5,OUTPUT);
  pinMode(stepPin6,OUTPUT);

  pinMode(dirPin1,OUTPUT);
  pinMode(dirPin2,OUTPUT);
  pinMode(dirPin3,OUTPUT);
  pinMode(dirPin4,OUTPUT);
  pinMode(dirPin5,OUTPUT);
  pinMode(dirPin6,OUTPUT);
  
  Serial.begin(9600);

  S1.setMaxSpeed(1000);  //maximum steps per second
  S1.setSpeed(50);       //steps per second
  S2.setMaxSpeed(1000);  //maximum steps per second
  S2.setSpeed(50);       //steps per second
  S3.setMaxSpeed(1000);  //maximum steps per second
  S3.setSpeed(50);       //steps per second
  S4.setMaxSpeed(1000);  //maximum steps per second
  S4.setSpeed(50);       //steps per second
  S5.setMaxSpeed(1000);  //maximum steps per second
  S5.setSpeed(50);       //steps per second
  S6.setMaxSpeed(1000);  //maximum steps per second
  S6.setSpeed(50);       //steps per second
}


//serial printing function with arbitrary types and arguments
void printLine()
{
  Serial.println();
}
template <typename T, typename... Types>
void printLine(T first, Types... other)
{
  Serial.print(first);
  printLine(other...);
}


void loop() {
  //call to potentially step motor once (constant speed)
  S1.runSpeed();
  S2.runSpeed();
  S3.runSpeed();
  S4.runSpeed();
  S5.runSpeed();
  S6.runSpeed();


  //Async communication
  if (Serial.available()>0 && c == '1'){
    c = Serial.read();
    printLine("recived:", c);
  }

  //communication response
  if (c == '0'){
    Serial.println("S1GO");
    c = '1';

    S1.move(200);   //positive should be clockwise
    S1.move(-200);  //negative should be anticlockwise
  
    } else if (c == '2'){
    Serial.println("S2GO");
    c = '1';

    S2.move(200);
    S2.move(-200);

    } else if (c == '3'){
    Serial.println("S3GO");
    c = '1';

    S3.move(200);
    S3.move(-200);

    } else if (c == '4'){
    Serial.println("S4GO");
    c = '1';

    S4.move(200);
    S4.move(-200);
  
    } else if (c == '5'){
    Serial.println("S5GO");
    c = '1';

    S5.move(200);
    S5.move(-200);

    } else if (c == '6'){
    Serial.println("S6GO");
    c = '1';

    S6.move(200);
    S6.move(-200);

  } else if (c != '1'){
    Serial.println("Clearing c");
    c = '1';
  }
  Serial.println("New iteration :)");
  delay(1000);
} 

//*
#include <AccelStepper.h>

const int stepsPerRevolution = 200;

const int dirPin1 = 12;
const int dirPin2 = 10;
const int dirPin3 = 8;
const int dirPin4 = 6;
const int dirPin5 = 4;
const int dirPin6 = 2;

const int stepPin1 = 13;
const int stepPin2 = 11;
const int stepPin3 = 9;
const int stepPin4 = 7;
const int stepPin5 = 5;
const int stepPin6 = 3;

AccelStepper S1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper S2(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper S3(AccelStepper::DRIVER, stepPin3, dirPin3);
AccelStepper S4(AccelStepper::DRIVER, stepPin4, dirPin4);
AccelStepper S5(AccelStepper::DRIVER, stepPin5, dirPin5);
AccelStepper S6(AccelStepper::DRIVER, stepPin6, dirPin6);

void setup() {
  Serial.begin(9600);

  S1.setMaxSpeed(5000);  // maximum steps per second
  S1.setSpeed(5000);       // steps per second
  S2.setMaxSpeed(4000);  // maximum steps per second
  S2.setSpeed(4000);       // steps per second
  S3.setMaxSpeed(3000);  // maximum steps per second
  S3.setSpeed(3000);       // steps per second
  S4.setMaxSpeed(2000);  // maximum steps per second
  S4.setSpeed(2000);       // steps per second
  S5.setMaxSpeed(1000);  // maximum steps per second
  S5.setSpeed(1000);       // steps per second
  S6.setMaxSpeed(1000);  // maximum steps per second
  S6.setSpeed(200);       // steps per second
} 

void loop() {
  // call to potentially step motor once (constant speed)
  if (S3.distanceToGo() == 0)
  {
    // Random change to speed, position and acceleration
    // Make sure we don't get 0 speed or accelerations
    S3.moveTo(random(200));
    S3.setMaxSpeed(random(200) + 1);
    S3.setAcceleration(random(200) + 1);

    S2.moveTo(random(200));
    S2.setMaxSpeed(random(200) + 1);
    S.setAcceleration(random(200) + 1);
  }
  S1.run();
  S2.run();
  S3.run();
  S4.run();
  S5.run();
  S6.run();
}
*//