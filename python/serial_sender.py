import serial
import time

def send_angle_sequence(
    sequence,
    port="COM3",  # Cambiar según sistema (COM3 en Windows, etc.)
    baudrate=115200,
    delay_between_steps=0.5
):
    """
    Send a sequence of [angle1, angle2, pen] commands to Arduino over serial.

    Args:
        sequence (list[list[int]]): List of [angle1, angle2, pen] steps
        port (str): Serial port
        baudrate (int): Baudrate for communication
        delay_between_steps (float): Seconds between steps
    """
    try:
        with serial.Serial(port, baudrate, timeout=2) as ser:
            print(f"🔌 Connected to {port}")
            time.sleep(2)  # Allow Arduino to reset

            for i, frame in enumerate(sequence):
                if len(frame) != 3:
                    print(f"⚠️ Invalid frame (must have 3 angles): {frame}")
                    continue

                line = " ".join(str(int(a)) for a in frame) + "\n"
                ser.write(line.encode())
                print(f"[{i+1}/{len(sequence)}] > Sent: {line.strip()}")

                ack = ser.readline().decode().strip()
                if ack == "OK":
                    print("✅ Arduino confirmed")
                else:
                    print(f"⚠️ No confirmation or error: '{ack}'")

                time.sleep(delay_between_steps)

    except Exception as e:
        print(f"❌ Serial communication error: {e}")

# Example usage
if __name__ == "__main__":
    angle_sequence = [
        [45, 90, 30],
        [50, 85, 90],
        [55, 80, 30]
    ]

    send_angle_sequence(angle_sequence, port="/dev/ttyUSB0")  # Cambiá según tu puerto
