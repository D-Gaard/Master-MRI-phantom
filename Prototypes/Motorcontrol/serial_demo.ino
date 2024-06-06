
void setup() {
  pinMode(13,OUTPUT);
  

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

char c = '1';

void loop() {
  //Async communication
  if (Serial.available()>0 && c == '1'){
    c = Serial.read();
    printLine("recived:", c);
  }

  //communication response
  if (c == '2'){
    Serial.println("d");
    c = '1';
  } else if (c == '3'){
    Serial.println("c");
    c = '1';
  } else if (c != '1'){
    Serial.println("Clearing c");
    c = '1';
  }
  Serial.println("New iteration :)");
  delay(1000);
} 
