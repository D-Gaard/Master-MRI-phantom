// This is very similar to Example 3 - Receive with start- and end-markers
//    in Serial Input Basics   http://forum.arduino.cc/index.php?topic=396450.0

const byte numChars = 64; //arduino uno is limited to 32 by default
char receivedChars[numChars];

boolean newData = false;

byte ledPin = 13;   // the onboard LED

//===============

void setup() {
    Serial.begin(115200);

    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
    digitalWrite(ledPin, HIGH);

    Serial.println("<Arduino is ready>");
}

//===============

void loop() {
    recvWithStartEndMarkers();
    replyToPython();
}

//===============

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

//===============

void replyToPython() {
    if (newData == true) {

        char firstChar;
        long numbers[6];
        long time;
        parseReceivedString(receivedChars, firstChar, numbers, time);

        Serial.print("<This just in ... ");
        Serial.print(receivedChars);
        Serial.print("   ");
        Serial.print(firstChar);

        for (int i = 0; i<6; i++){
          Serial.print("   ");
          Serial.print(numbers[i]);
        }
        Serial.print("   ");
        Serial.print(time);
        Serial.print("   ");
        Serial.print(millis());
        Serial.print('>');
  
        // change the state of the LED everytime a reply is sent
        digitalWrite(ledPin, ! digitalRead(ledPin));
        newData = false;
    }
}

//parse the motor string (format described in serial_mc_integration.ipynb)
void parseReceivedString(char* receivedString, char& firstChar, long numbers[], long& value) {
  // Extract the first character
  firstChar = receivedString[0];

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
//===============