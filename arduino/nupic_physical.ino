/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
 */

int value = 0; //integer for prediction value
String inString = "";    // string to hold input

void setup() {
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  //read the values from the photocells
  Serial.print(analogRead(0));
  Serial.print(",");
  Serial.print(analogRead(1));
  Serial.print(",");
  Serial.print(analogRead(2));
  Serial.print(",");
  Serial.print(analogRead(3));
  Serial.println();

  //collects digits from the prediction feedback and converts them into an integer for "writing" to the led
  //maybe there is a better way to do this
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      // convert the incoming byte to a char
      // and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string,
    // then the string's value:
    if (inChar == '\n') {
      value = inString.toInt();
      // clear the string for new input:
      inString = "";
      //write the value to the led
      analogWrite(9, value/4);
    }
  }
  //take a sample every 1/2 second
  delay(500);
}

