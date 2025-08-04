# AI Arm Drawing 🤖✍️
AI-powered robotic arm that draws based on natural language instructions.

## Description
**AI Arm Drawing** is a robotic arm project powered by Artificial Intelligence that can draw based on natural language instructions.  
The system uses an Arduino-controlled 4DOF robotic arm to hold a pen and create shapes, patterns, or sketches.  
A Python program sends user prompts to an AI model (such as OpenAI’s GPT) to convert them into simple movement commands.  
These commands are then sent to the robotic arm, allowing it to draw autonomously.

This project combines **robotics**, **AI-powered instruction parsing**, and **servo-based motion control**.  
It’s an ideal starting point for experimenting with AI-driven hardware interactions, creative robotics, and physical computing.

---

## Features
- Converts natural language into drawing commands.
- Controls a 4DOF robotic arm with Arduino.
- Supports easy calibration and manual control via joystick.
- Modular Python and Arduino code for easy extension.

---

## Possible Applications
- AI-assisted art creation.
- Educational robotics.
- Automated sketching and diagram drawing.

---

## Project Structure
```text
ai-arm-drawing/
│
├── arduino/
│   └── robotic_hand.ino      # Arduino code to control servos
│
├── python/
│   ├── main.py               # Main Python script
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
- Arduino UNO (included in kit)
- 4DOF robotic arm with servos (MG90S)
- Joystick controller (optional for manual control)
- USB cable for Arduino
- 5V power supply for servos

### 2. Software Requirements
- Arduino IDE
- Python 3.9+  
- OpenAI API key

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
This project is licensed under the MIT License - see the LICENSE file