# ENCS3320 - Computer Networks Project 1

## Overview
This project consists of the first two tasks of the **ENCS3320: Computer Networks** course. It demonstrates the fundamental concepts of web development (HTML/CSS) and socket programming in Python to create a custom HTTP Web Server.

---

## 🛠 Task 1: Web Design and Content
The objective of this task was to design a responsive and multi-lingual (English and Arabic) website that serves as the front-end for our web server.

### Features:
- **Multi-lingual Support**: Full support for English (`main_en.html`) and Arabic (`main_ar.html`) with localized content.
- **Responsive Design**: Styled using Vanilla CSS (`style.css`) to ensure compatibility across different screen sizes.
- **Modern UI/UX**: Includes a navigation bar, hero section, team profiles, and an educational section about Network Security.
- **Dynamic Elements**: 
  - Welcome text styled with CSS.
  - Custom favicon generated via JavaScript on page load.
  - Interactive FontAwesome icons.

### Key Pages:
- `main_en.html` / `main_ar.html`: The primary landing pages.
- `mySite_1222274_en.html` / `mySite_1222274_ar.html`: Specific pages for media requests and student information.
- `style.css`: The central stylesheet for the entire project.

---

## 🖥 Task 2: Python HTTP Web Server
The objective of this task was to implement a functional HTTP server from scratch using Python's `socket` library, without using high-level frameworks like Flask or Django.

### Functionalities:
1. **Basic HTTP GET Requests**: Handles incoming TCP connections and parses HTTP request lines to identify the requested file.
2. **Static File Serving**: Serves various file types including:
   - **HTML** (`text/html`)
   - **CSS** (`text/css`)
   - **Images** (`image/png`, `image/jpeg`)
   - **Videos** (`video/mp4`)
3. **Advanced Routing**: 
   - Supports default paths (e.g., `/` redirects to `main_en.html`).
   - Handles language-specific routing.
4. **Error Handling (404 Not Found)**: Provides a custom HTML error page that displays the client's IP and Port when a requested file does not exist.
5. **Smart Redirection (307 Temporary Redirect)**: 
   - If a requested file (image, video, or general file) is not found locally, the server redirects the client to a Google Search (or Image/Video search) for that specific filename.
6. **Logging**: Real-time console logging of client connections, request details, and server responses.

---

## 🚀 How to Run

### Prerequisites:
- Python 3.x installed.

### Steps:
1. Navigate to the `Task2` directory:
   ```bash
   cd Task2
   ```
2. Run the web server:
   ```bash
   python webserver.py
   ```
3. Open your browser and visit:
   - [http://127.0.0.1:9927/](http://127.0.0.1:9927/)

---

## 👥 Team Members
- **Husam Atwan** (1222274)
- **Anwar Atawneh** (1222275)
- **Quasi Abu Sondos** (1221082)

---

## 📚 Resources
- Textbook: *Computer Networking: A Top-Down Approach* (Kurose & Ross).
- University: Birzeit University.
