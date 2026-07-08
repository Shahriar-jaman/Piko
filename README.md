# PIKO: A Portable Spy Bot with Multi-Detection System

## Project Overview

In an increasingly unpredictable world, personal security and situational awareness are paramount. Traditional surveillance systems (CCTV) are static, expensive, and leave "blind spots," while current portable cameras (like dashcams) are passive and lack real-time threat detection capabilities. 

**Piko** is an intelligent, portable, and active personal security companion designed to fill this gap. Built for an Operating Systems course (CSE-323) at North South University, Piko acts as an autonomous security guard. It utilizes a distributed computing approach, balancing the portability of a microcontroller with the processing power of a host PC to deliver real-time object detection and automated alerts.

## Key Features

* **Active Vision (The Eye):** Piko features a 180° scanning "neck" powered by a servo motor, eliminating traditional blind spots by actively sweeping its surroundings.
* **Intelligent Threat Detection (The Brain):** The video feed is processed in real-time by a YOLOv3 neural network running on a host computer. It can distinguish between a benign presence and potential threats by identifying classes like 'Person', 'Knife', 'Pistol', 'Rifle', and 'Scissors' with a 50% confidence threshold.
* **Rapid Response & Alert Protocol:** Upon threat detection, Piko captures a high-resolution snapshot and instantly sends an SMTP email alert to a designated security address. A smart 60-second cooldown prevents spamming.
* **Visual Deterrence:** A fading "breathing" LED eye and the active scanning motion signal that the area is being monitored.
* **Portable & Versatile:** Equipped with a magnetic base, Piko can easily transition from a wearable shoulder mount to a stationary guard on a metallic surface (like a door or fridge).

## System Architecture & Approach

The project uses a Distributed Computing Approach:
1.  **Hardware (The Body):** An ESP32 microcontroller manages the physical behaviors, controlling the servo motor (scanning) and the LED (breathing effect). A breadboard power supply ensures stable 5V power.
2.  **Vision (The Eye):** An ESP32-CAM module acts as an IP camera, streaming MJPEG video and handling multi-resolution endpoints over Wi-Fi.
3.  **Intelligence (The Brain):** A Python script running on a host PC fetches the video feed and runs the YOLOv3 model to analyze frames, handling the heavy AI computation and the SMTP alert logic.

## Hardware Components

* ESP32 Microcontroller
* ESP32-CAM Module
* Servo Motor (0°–180° rotation)
* LED
* Breadboard Power Supply (5V)
* Magnetic Base

## Software Stack

* **Firmware:** C++ (ESP32 Web Server & HTTP requests)
* **Processing:** Python (Host PC Control Script)
* **AI/ML:** YOLOv3 (Object Detection) & NMS (Non-Maximum Suppression)

## Team Members

* **Shahriar Jaman (AI & Software Lead):** Developed the object detection brain, Python control script, YOLOv3 implementation, and SMTP email logic.
* **Sudipta Karmaker (Firmware & Network Engineer):** Developed the wireless vision system, C++ firmware, multi-resolution stream endpoints, and MJPEG optimization.
* **Anindita Tabassum Lubaba (Hardware Integration):** Led mechanical design, assembly, circuit design, servo/LED behavioral coding, and power distribution management.

## Next Steps & Future Improvements

* **Edge AI:** Move the object detection directly onto the ESP32 using TensorFlow Lite for Microcontrollers for full standalone, wireless operation.
* **Facial Recognition:** Implement features to distinguish between the "Owner" and "Unknown Intruders" to minimize false alarms.
* **Audio Deterrent:** Add a buzzer or speaker to emit a siren sound when a weapon is detected.
* **Enclosure Design:** Create a 3D-printed shell to hide wiring, protect components, and make Piko weather-resistant.
* **Power Optimization:** Integrate a LiPo battery with a boost converter for true portability without relying on a breadboard power supply.
