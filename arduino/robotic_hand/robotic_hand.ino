#include <Servo.h>

// Servo declarations
Servo leftShoulder;    // Servo 1
Servo rightShoulder;   // Servo 2
Servo pen;             // Pen up/down

// Pin definitions
const int SERVO_1_PIN = 9;
const int SERVO_2_PIN = 8;
const int PEN_SERVO_PIN = 7;

void setup() {
  Serial.begin(115200);

  // Attach servos to pins
  leftShoulder.attach(SERVO_1_PIN);
  rightShoulder.attach(SERVO_2_PIN);
  pen.attach(PEN_SERVO_PIN);

  // Initial neutral positions
  leftShoulder.write(90);
  rightShoulder.write(90);
  pen.write(90); // Pen up by default
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.length() == 0) return;

    int angle1, angle2, penAngle;

    // Parse string into three integers
    int parsed = sscanf(line.c_str(), "%d %d %d", &angle1, &angle2, &penAngle);

    if (parsed == 3 &&
        angle1 >= 0 && angle1 <= 180 &&
        angle2 >= 0 && angle2 <= 180 &&
        penAngle >= 0 && penAngle <= 180) {

      leftShoulder.write(angle1);
      rightShoulder.write(angle2);
      pen.write(penAngle);

      delay(100);  // Give time for servos to reach target

      Serial.println("OK");
    } else {
      Serial.println("ERROR");
    }
  }
}
