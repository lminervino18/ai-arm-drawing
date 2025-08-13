#include <Servo.h>

// =====================
// Pin configuration
// =====================
#define SERVO_1_PIN     9
#define SERVO_2_PIN     8
#define PEN_SERVO_PIN   7

// =====================
// Servo limits & setup
// =====================
#define INIT_POS            90
#define MAX_SERVO_CONFIG   180
#define MIN_SERVO_1         50
#define MAX_SERVO_2        (MAX_SERVO_CONFIG - MIN_SERVO_1)

// Optional small settling delay after writes (ms)
#define SERVO_SETTLE_MS     15

// Servo instances
Servo leftShoulder;
Servo rightShoulder;
Servo pen;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500); // Read timeout for readStringUntil

  leftShoulder.attach(SERVO_1_PIN);
  rightShoulder.attach(SERVO_2_PIN);
  pen.attach(PEN_SERVO_PIN);

  leftShoulder.write(INIT_POS);
  rightShoulder.write(INIT_POS);
  pen.write(INIT_POS);

  // Optional: announce ready
  // Serial.println("READY");
}

void loop() {
  if (!Serial.available()) return;

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  int angle1, angle2, penAngle;

  // Parse "a b c"
  int parsed = sscanf(line.c_str(), "%d %d %d", &angle1, &angle2, &penAngle);

  // Validate ranges
  bool rangesOk =
      (angle1 >= MIN_SERVO_1 && angle1 <= MAX_SERVO_CONFIG) &&
      (angle2 >= 0           && angle2 <= MAX_SERVO_2) &&
      (penAngle >= 0         && penAngle <= 180);

  if (parsed == 3 && rangesOk) {
    // Write positions
    leftShoulder.write(angle1);
    rightShoulder.write(angle2);
    pen.write(penAngle);

    // Small settle; main pacing should be controlled by the host (Python)
    if (SERVO_SETTLE_MS > 0) delay(SERVO_SETTLE_MS);

    Serial.println("OK");
  } else {
    // Build a simple error message to help debugging on the host
    if (parsed != 3) {
      Serial.println("ERROR: PARSE");
    } else {
      Serial.print("ERROR: RANGE ");
      Serial.print(angle1); Serial.print(' ');
      Serial.print(angle2); Serial.print(' ');
      Serial.println(penAngle);
    }
  }
}
