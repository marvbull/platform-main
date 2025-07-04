# 🛠️ 3-DoF Stewart Platform

## 📖 Project Overview

This project was developed for **MTE 380 at the University of Waterloo**.  
It features a custom **3-DOF Stewart platform** designed to **automatically detect, center, and balance a ball** in real time.

The system combines **mechanical design**, **embedded control**, and **computer vision** into a fully integrated mechatronic solution.  
Special focus was placed on **real-time computing** and **closed-loop control** using a **PID controller** for fast and stable balancing.

## 🎬 Demonstration Videos

- ▶️ **First Iteration**: (https://www.youtube.com/watch?v=eKMGxfKeExc)
- ✅ **Final Presentation**: https://www.youtube.com/watch?v=GQNaFhVhSu0


## 📂 Repository Structure

- `src/` – Core control code (C++, Arduino)  
- `vision/` – Image processing and ball tracking (OpenCV)  
- `cad/` – Mechanical models and drawings (Fusion360, Solidworks)  
- `docs/` – System documentation, control design, and test results  
- `README.md` – Project overview

## ⚙️ Technologies Used

- **OpenCV (Python/C++)** – Ball detection and tracking  
- **PID Controller** – Real-time feedback control for platform stabilization  
- **C++ / Arduino** – Servo control and logic implementation  
- **MATLAB** – System modeling and controller tuning  
- **Solidworks** – Mechanical design  
- **I²C or Serial** – Communication between vision and control units

## 🧠 Control Strategy

A **2-axis PID controller** (X and Y) was implemented to keep the ball centered on the platform.  
The ball’s position is detected via computer vision, and the platform adjusts its tilt accordingly in real time.

- Tuned manually based on system response  
- Executed on microcontroller with fixed control loop  
- Achieves fast reaction with minimal overshoot

## 🚀 Project Status

✅ **Completed**  
All components were developed, integrated, and tested.  
The platform successfully performs **real-time ball tracking and balancing** using PID control.

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.
