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
#define MIN_SERVO_1         30
#define MAX_SERVO_2        (MAX_SERVO_CONFIG - MIN_SERVO_1)

#define SERVO_SETTLE_MS     15
#define SMOOTH_STEP_DELAY   5   // ms between steps
#define SMOOTH_STEP_SIZE    1   // degrees per step

#define INACTIVITY_TIMEOUT_MS 3000  // 3 segundos

Servo leftShoulder;
Servo rightShoulder;
Servo pen;

unsigned long lastCommandTime = 0;
bool returnedHome = false;

void smoothMove(Servo& servo, int fromAngle, int toAngle) {
  int step = (toAngle > fromAngle) ? SMOOTH_STEP_SIZE : -SMOOTH_STEP_SIZE;
  for (int angle = fromAngle; angle != toAngle; angle += step) {
    servo.write(angle);
    delay(SMOOTH_STEP_DELAY);
  }
  servo.write(toAngle);
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);

  leftShoulder.attach(SERVO_1_PIN);
  rightShoulder.attach(SERVO_2_PIN);
  pen.attach(PEN_SERVO_PIN);

  leftShoulder.write(INIT_POS);
  rightShoulder.write(INIT_POS);
  pen.write(INIT_POS);

  lastCommandTime = millis();
}

void loop() {
  // Si pasó el tiempo sin recibir comandos y aún no volvió a home
  if ((millis() - lastCommandTime > INACTIVITY_TIMEOUT_MS) && !returnedHome) {
    smoothMove(pen, pen.read(), INIT_POS);
    smoothMove(leftShoulder, leftShoulder.read(), INIT_POS);
    smoothMove(rightShoulder, rightShoulder.read(), INIT_POS);
    returnedHome = true;
    Serial.println("TIMEOUT: RETURNED TO HOME");
    return;
  }

  if (!Serial.available()) return;

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  int angle1, angle2, penAngle;
  int parsed = sscanf(line.c_str(), "%d %d %d", &angle1, &angle2, &penAngle);

  bool rangesOk =
      (angle1 >= MIN_SERVO_1 && angle1 <= MAX_SERVO_CONFIG) &&
      (angle2 >= 0           && angle2 <= MAX_SERVO_2) &&
      (penAngle >= 0         && penAngle <= 180);

  if (parsed == 3 && rangesOk) {
    angle1 = constrain(angle1, MIN_SERVO_1, MAX_SERVO_CONFIG);
    angle2 = constrain(angle2, 0, MAX_SERVO_2);
    penAngle = constrain(penAngle, 0, MAX_SERVO_CONFIG);

    int current1 = leftShoulder.read();
    int current2 = rightShoulder.read();
    int currentPen = pen.read();

    smoothMove(leftShoulder, current1, angle1);
    smoothMove(rightShoulder, current2, angle2);
    smoothMove(pen, currentPen, penAngle);

    if (SERVO_SETTLE_MS > 0) delay(SERVO_SETTLE_MS);

    Serial.println("OK");

    // Reset timer y home flag
    lastCommandTime = millis();
    returnedHome = false;
  } else {
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
