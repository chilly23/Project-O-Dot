# O-dot: Hands-Free Eye-Tracking Interface with Smart Ring Control

O-dot is a hybrid hardware-software interface that replaces the traditional mouse using just your eyes and a smart ring. The system lets users control a computer cursor by tracking their gaze through a webcam and execute mouse actions using a finger-worn smart ring. Ideal for accessibility, productivity, and even couch computing.

---

## What It Does

- Uses webcam-based gaze tracking to detect where the user is looking on the screen.
- A smart ring with three physical buttons maps to left-click, right-click, and scroll interactions.
- Users simply look at an element on screen and click via their ring—no need to move a mouse or touch a trackpad.

---

## Why This Exists

Current interfaces like mouse and touchpad aren’t practical for all environments—TVs, AR/VR, physically challenged users, or even when you're lying back and don't want to move. O-dot reimagines human-computer interaction for accessibility, convenience, and futuristic interaction.

---

## Tech Stack

- **Eye Tracking**: OpenCV + ML model trained on real-time gaze data
- **Smart Ring**: Arduino-based device with 3-button interface via serial communication
- **Backend**: Python for gaze capture and UI coordination
- **Frontend**: PyAutoGUI for cursor control and interaction emulation

---

## Features

- Gaze-based pointer movement
- Smart ring-based clicking (Left, Right, Scroll)
- ML-based prediction for accurate gaze-to-cursor mapping
- Minimal setup—just a webcam and the ring

---

## 🛠Hardware Components

- Arduino Nano / Uno
- 3 x Push buttons
- Lithium battery or USB power supply
- Bluetooth / Serial module (optional for wireless mode)
- 3D-printed ring case (optional)

---
