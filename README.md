# AI-Air-Writing-Correction-Assistant
This project is a contactless writing interface that allows users to write in the air using hand gestures captured by a webcam. It utilizes Computer Vision (OpenCV) and Deep Learning to track finger movements and recognize alphanumeric characters in real-time.
# ✍️ AI Air Writing & Correction Assistant

**Turn your finger into a digital pen.** This application uses Computer Vision to track hand gestures, convert them into digital text, and polish the results using Generative AI.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-red.svg)
![Gemini](https://img.shields.io/badge/AI-Google_Gemini-orange.svg)

## 🚀 Overview

The **Air Writing Assistant** solves the problem of contactless text input. By tracking the index finger, users can draw characters on a virtual canvas. The system predicts the character using a trained CNN model and assembles sentences.

When the camera session ends, the raw text is sent to **Google Gemini**, which fixes grammar, spelling, and sentence structure inconsistencies. The final polished text is saved to a local database and accessible via a clean **Django Web Interface**.

## ✨ Key Features

* **Real-time Hand Tracking:** Uses MediaPipe & OpenCV to detect finger landmarks with high precision.
* **Gesture Controls:**
    * 👆 **Index Finger:** Write/Draw.
    * ✌️ **Two Fingers:** Select Menu / Pause Writing.
    * 👍 **Thumb Up:** Confirm Word.
    * ✊ **Fist:** Clear Canvas.
* **AI Character Recognition:** Custom Deep Learning models for Alphabets and Numbers.
* **Smart Post-Processing:** Integration with **Gemini 1.5 Flash** to correct raw sentence output automatically.
* **Web Dashboard:** A Django-based UI to manage saved sessions (View, Rename, Download, Delete).
* **Visual Feedback:** Real-time overlay of the virtual canvas on the camera feed using Pygame.

## 🛠️ Tech Stack

* **Core:** Python
* **Computer Vision:** OpenCV, MediaPipe, HandTrackingModule
* **GUI & Interaction:** Pygame, NumPy
* **Backend:** Django (SQLite)
* **AI/LLM:** Google Gemini API (Generative AI), TensorFlow/Keras (Character Recognition)
* **Frontend:** HTML, TailwindCSS (Glassmorphism UI)

## 📸 Workflow

1.  **Capture:** Webcam tracks the index finger tip.
2.  **Predict:** The stroke is converted to an image and fed to the CNN model.
3.  **Refine:** `spellchecker` fixes words locally; `Gemini API` fixes sentences globally.
4.  **Store:** Text is saved to disk and indexed in the Django database.
5.  **Manage:** User accesses the files via the web portal.
