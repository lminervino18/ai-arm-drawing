from serial_sender import send_angle_sequence

def main():
    # Example usage
    angle_sequence = [(120, 45, 125), (120, 30, 125), (100, 30, 125), (100, 45, 125), (120, 45, 125)]
    send_angle_sequence(angle_sequence)

if __name__ == "__main__":
    main()
