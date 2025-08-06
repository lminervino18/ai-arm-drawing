# 🤖 AI Drawing Arm

AI-powered robotic arm that interprets natural language prompts and draws symbolic figures on a 14×10 grid whiteboard.

---

## 📝 Project Description

**AI Drawing Arm** is a robotic system that takes natural language prompts (like "draw a frog") and autonomously creates symbolic drawings on a 14×10 grid (7×5 cm) whiteboard.  
The pipeline uses generative AI (OpenAI or Gemini) to convert user prompts into vector-based instructions, then applies inverse kinematics to control a dual-arm mechanical structure with two servo motors.

This project combines **natural language processing**, **motion planning**, and **hardware control** to simulate intelligent robotic drawing.

---

## 🧩 How It Works

1. **Input:**  
   The user writes a prompt (e.g., "draw a square").

2. **AI Translation:**  
   An AI model returns a list of vector drawing instructions, e.g.:
   ```
   0 2 3
   1 4 0
   1 0 4
   1 -4 0
   ```
   - Each line: `<draw_flag> <delta_x> <delta_y>`
   - The pen starts at (0, 0) (bottom-left of the grid).

3. **Validation:**  
   Instructions are checked to ensure they stay within a 14×10 grid (7×5 cm) and are well-formed.

4. **Kinematics:**  
   Each grid position is converted to (x, y) in cm and mapped to servo angles using inverse kinematics.

5. **Output:**  
   A set of angles and pen commands is generated to control the robot arm.

---

## 🔧 Hardware Setup

The system simulates or controls a 2-arm robotic mechanism, each with 2 degrees of freedom:

| Arm       | Segment 1 (Upper) | Segment 2 (Lower) | Servo Mount Location |
|-----------|-------------------|-------------------|---------------------|
| Left Arm  | 6.0 cm            | 6.0 cm            | (5.0 cm, 5.0 cm)    |
| Right Arm | 6.0 cm            | 6.0 cm            | (10.0 cm, 5.0 cm)   |

- Each arm consists of two servos (total 4 servos).
- The tip of both arms converges on a shared pen mechanism.
- A microcontroller (e.g., Arduino or ESP32) actuates the motors based on the calculated angles.

---

## 🛠️ Software Stack

- **Python:** Core logic (Tkinter GUI, instruction validation, inverse kinematics)
- **OpenAI / Gemini API:** Natural language processing and drawing generation
- **NumPy:** Vector math for arm positioning
- **Tkinter:** Optional GUI for previewing drawings
- **Serial (optional):** To send angles to a physical robot

---

## Features

- Converts natural language into drawing commands
- Validates instructions to ensure safe, in-bounds operation
- Inverse kinematics for dual-arm control
- Controls a 4DOF robotic arm with Arduino or ESP32
- Supports easy calibration and manual control via joystick
- Modular Python and Arduino code for easy extension

---

## Possible Applications

- AI-assisted art creation
- Educational robotics
- Automated sketching and diagram drawing

---

## High-Level Architecture

![High-level diagram](design/high-level-diagram.jpg)

```text
User Prompt
    │
    ▼
AI Model (OpenAI/Gemini)
    │
    ▼
Drawing Instructions (vector format)
    │
    ▼
Validation & Kinematics (Python)
    │
    ▼
Servo Angles & Pen Commands
    │
    ▼
Robotic Arm (Arduino/ESP32)
```

---

## Project Structure
```text
ai-arm-drawing/
│
├── arduino/
│   └── robotic_hand.ino      # Arduino code to control servos
│
├── python/
│   ├── main.py               # Main Python script (prompt, validation, kinematics)
│   ├── ai_client.py          # AI API integration
│   ├── serial_client.py      # Serial communication with Arduino
│   └── requirements.txt      # Python dependencies
│
├── README.md                 # Project documentation
├── .gitignore                # Git ignore rules
└── LICENSE                   # Project license
```

---

## Getting Started

### 1. Hardware Requirements
- Arduino UNO or ESP32
- 4DOF robotic arm with servos (MG90S or similar)
- Joystick controller (optional for manual control)
- USB cable for Arduino/ESP32
- 5V power supply for servos

### 2. Software Requirements
- Arduino IDE
- Python 3.9+  
- OpenAI or Gemini API key

### 3. Install Python dependencies
```bash
pip install -r python/requirements.txt
```

### 4. Set your API key
```bash
export OPENAI_API_KEY="your_api_key_here"  # Linux/Mac
set OPENAI_API_KEY="your_api_key_here"     # Windows
```

### 5. Upload Arduino code
Open `arduino/robotic_hand.ino` in Arduino IDE, select your board and port, then upload.

### 6. Run the Python script
```bash
python python/main.py
```

---

## License
This project is licensed under the MIT License - see the LICENSE file.