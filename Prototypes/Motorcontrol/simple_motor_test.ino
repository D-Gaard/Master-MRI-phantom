#include <Stepper.h>

char c = '1';
const int stepsPerRevolution = 200;

const int dirPin1 = 3;
const int stepPin1 = 2;
const int dirPin2 = 5;
const int stepPin2 = 4;
const int dirPin3 = 7;
const int stepPin3 = 6;
const int dirPin4 = 9;
const int stepPin4 = 8;
const int dirPin5 = 11;
const int stepPin5 = 10;
const int dirPin6 = 13;
const int stepPin6 = 12;
Stepper S1(stepsPerRevolution, dirPin1, stepPin1);
Stepper S2(stepsPerRevolution, dirPin2, stepPin2);
Stepper S3(stepsPerRevolution, dirPin3, stepPin3);
Stepper S4(stepsPerRevolution, dirPin4, stepPin4);
Stepper S5(stepsPerRevolution, dirPin5, stepPin5);
Stepper S6(stepsPerRevolution, dirPin6, stepPin6);

//Stepper stepper(stepsPerRevolution, 13, 12);



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
}

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

//+ -> counter cw
//- -> cw
int step_val = -100;
int step_speed = 100;

void loop() {
  //Async communication
  if (Serial.available()>0 && c == '1'){
    c = Serial.read();
    printLine("recived:", c);
  }

  //communication response
  if (c == '0'){
    Serial.println("S1GO");
    c = '1';
    S1.setSpeed(step_speed);
    S1.step(step_val);
    //S1.step(-200);
  
    } else if (c == '2'){
    Serial.println("S2GO");
    c = '1';
    S2.setSpeed(step_speed);
    S2.step(step_val);
    //S2.step(-200);

    } else if (c == '3'){
    Serial.println("S3GO");
    c = '1';
    S3.setSpeed(step_speed);
    S3.step(step_val);
    //S3.step(-200);

    } else if (c == '4'){
    Serial.println("S4GO");
    c = '1';
    S4.setSpeed(step_speed);
    S4.step(step_val);
    //S4.step(-200);
  
    } else if (c == '5'){
    Serial.println("S5GO");
    c = '1';
    S5.setSpeed(step_speed);
    S5.step(step_val);
    //S5.step(-200);

    } else if (c == '6'){
    Serial.println("S6GO");
    c = '1';
    S6.setSpeed(step_speed);
    S6.step(step_val);
    //S6.step(-200);

  } else if (c != '1'){
    Serial.println("Clearing c");
    c = '1';
  }
  Serial.println("New iteration :)");
  delay(1000);
} 
