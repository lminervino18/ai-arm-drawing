from serial_sender import send_angle_sequence

def main():
    angle_sequence = [
        [140, 80, 125],
        [150, 60, 125],
        [160, 65, 125],
        [170, 45, 90]
    ]

    send_angle_sequence(angle_sequence)

if __name__ == "__main__":
    main()