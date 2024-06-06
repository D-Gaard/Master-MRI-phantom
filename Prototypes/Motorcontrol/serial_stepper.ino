#include <Stepper.h>

char c = '1';
const int stepsPerRevolution = 200;
Stepper stepper(stepsPerRevolution, 13, 12);
const int dirPin = 13;
const int stepPin = 12;

void setup() {
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);
  
  
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


void loop() {
  //Async communication
  if (Serial.available()>0 && c == '1'){
    c = Serial.read();
    printLine("recived:", c);
  }

  //communication response
  if (c == 'f'){
    Serial.println("forward");
    c = '1';
    stepper.setSpeed(100); // Set the speed (adjust as needed)
    stepper.step(200); 

  } else if (c == 'b'){
    Serial.println("bakwards");
    c = '1';
    stepper.setSpeed(100); // Set the speed (adjust as needed)
    stepper.step(-200); 
    
  } else if (c != '1'){
    Serial.println("Clearing c");
    c = '1';
  }
  Serial.println("New iteration :)");
  delay(1000);
} 
