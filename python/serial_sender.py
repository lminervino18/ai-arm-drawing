import serial
import time


def send_angle_sequence(
    sequence: list[list[float]],
    port: str = "COM3",
    baudrate: int = 115200,
    delay_between_steps: float = 0.5
):
    """
    Sends a sequence of [angle1, angle2, pen] commands to Arduino over serial.

    Args:
        sequence: List of [angle1, angle2, pen] steps
        port: Serial port name (e.g., COM3, /dev/ttyUSB0)
        baudrate: Serial baud rate
        delay_between_steps: Seconds to wait between sending steps
    """
    try:
        with serial.Serial(port, baudrate, timeout=2) as ser:
            print(f"🔌 Connected to {port}")
            time.sleep(2)  # Wait for Arduino reset

            for i, frame in enumerate(sequence):
                if len(frame) != 3:
                    print(f"⚠️ Invalid frame (must have 3 values): {frame}")
                    continue

                line = " ".join(str(int(a)) for a in frame) + "\n"
                ser.write(line.encode())
                print(f"[{i+1}/{len(sequence)}] > Sent: {line.strip()}")

                ack = ser.readline().decode().strip()
                if ack == "OK":
                    print("✅ Arduino confirmed")
                else:
                    print(f"⚠️ No confirmation or unexpected reply: '{ack}'")

                time.sleep(delay_between_steps)

    except Exception as e:
        print(f"❌ Serial communication error: {e}")


# Example for standalone testing
if __name__ == "__main__":
    angle_sequence = [
        [45, 90, 30],
        [50, 85, 90],
        [55, 80, 30]
    ]

    send_angle_sequence(angle_sequence, port="/dev/ttyUSB0")
