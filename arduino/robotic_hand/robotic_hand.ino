#include <Servo.h>

// Pins

#define SERVO_1_PIN 9
#define SERVO_2_PIN 8
#define PEN_SERVO_PIN 7

// Servos

#define INIT_POS 90
#define NUM_SERVOS 3
#define MAX_SERVO_CONFIG 180
#define MIN_SERVO_1 50
#define MAX_SERVO_2 (MAX_SERVO_CONFIG - MIN_SERVO_1)
#define SERVO_UP 90
#define SERVO_WRITE 125 


// Servo declarations
Servo leftShoulder;
Servo rightShoulder;  
Servo pen;            

void setup() {
  // Baud Rate
  Serial.begin(115200);

  // Attach servos to pins
  leftShoulder.attach(SERVO_1_PIN);
  rightShoulder.attach(SERVO_2_PIN);
  pen.attach(PEN_SERVO_PIN);

  // Initial positions
  leftShoulder.write(INIT_POS);
  rightShoulder.write(INIT_POS);
  pen.write(INIT_POS); 
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.length() == 0) return;

    int angle1, angle2, penAngle;

    // Parse string into three integers
    int parsed = sscanf(line.c_str(), "%d %d %d", &angle1, &angle2, &penAngle);

    if (parsed == NUM_ANGLES &&
       (angle1 >= MIN_SERVO_1 && angle1 <= MAX_SERVO_CONFIG) &&
       (angle2 >= 0 && angle2 <= MAX_SERVO_2) &&
       (penAngle == SERVO_UP || penAngle == SERVO_WRITE) &&
       ((angle1 - angle2) > 0)) {
        
      
      leftShoulder.write(angle1);
      rightShoulder.write(angle2);
      pen.write(penAngle); 
      
      Serial.println("OK");
    } else 
      Serial.println("ERROR");
    
  }

  delay(100);
}
