#include <Servo.h>

Servo thumb, index, middle, ring, pinky ;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int mindValue = 0;


void setup() {
  thumb.attach(8);
  index.attach(9);  
  middle.attach(10);  
  ring.attach(11);  
  pinky.attach(12);  
  Serial.begin(9600);
  restFingers();
}


void loop() {
  Serial.println("Please enter a number between 1 and 5, or 99.");
  while(Serial.available() == 0){
  }
  mindValue = Serial.parseInt();
  if (mindValue >= 1 && mindValue <= 5) { 
    processMindValue(mindValue);
  }else if (mindValue == 99) { 
    processConcentration();
  }
}

// this function shows the fingers based on the number of blinks received
void processMindValue(int mValue) {
    for (pos = 60; pos <= 150; pos += 2) { // goes from 60 degrees to 120 degrees
      // in steps of 1 degree
      showFingers(pos, mValue);
      delay(15);                       // waits 15ms for the servo to reach the position
    }
    delay(2000); 
    for (pos = 150; pos >= 60; pos -= 1) { // goes from 120 degrees to 60 degrees
      showFingers(pos, mValue);  
      delay(15);                       // waits 15ms for the servo to reach the position
    }
}

void showFingers(int pos, int mValue){
   switch(mValue) {
    case 1:
       index.write(pos);  
       break;
    case 2:
       index.write(pos);  
       middle.write(pos);  
       break;
    case 3:
       index.write(pos);  
       middle.write(pos);  
       ring.write(pos);  
       break;
    case 4:
       index.write(pos);  
       middle.write(pos);  
       ring.write(pos);  
       pinky.write(pos); 
       break;
    case 5:
       thumb.write(210 - pos);
       index.write(pos);  
       middle.write(pos);  
       ring.write(pos);  
       pinky.write(pos); 
       break;
    default:
       Serial.println("Invalid input. Please enter a number between 1 and 5, or 99.");
  } 
}


// this function moves the fingers in a wavy pattern if the conentration number is received, the concentration number expected is 99.
void processConcentration() {
  Serial.println("Showing wavy finger pattern");
  int posThumb, posIndex, posMiddle, posRing, posPinky;
  int offset = 40; // Offset between finger positions

  int currentCount = 1;
  int maxWaveCount = 250;
  for (int i = 180; i > 0; i += 4) {
    posThumb = sin(i * PI / 180.0) * 40 + 90;
    posIndex = sin((i + offset) * PI / 180.0) * 40 + 90;
    posMiddle = sin((i + 2 * offset) * PI / 180.0) * 40 + 90;
    posRing = sin((i + 3 * offset) * PI / 180.0) * 40 + 90;
    posPinky = sin((i + 4 * offset) * PI / 180.0) * 40 + 90;

    thumb.write(posThumb);
    index.write(posIndex);
    middle.write(posMiddle);
    ring.write(posRing);
    pinky.write(posPinky);
    Serial.print("Showing second half");
    Serial.println(posThumb);
    Serial.println(posIndex);
    Serial.println(posMiddle);
    Serial.println(posRing);
    Serial.println(posPinky);
    if(currentCount == maxWaveCount){
      break;
    }
    currentCount += 1;
    delay(15);
  }
  restFingers();
}



void restFingers(){
    thumb.write(150);
    index.write(60);
    middle.write(60);
    ring.write(60);
    pinky.write(60);
}
