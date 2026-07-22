# keshavkumar07.github.io

# 🎓 Face Recognition Attendance System

A simple and user-friendly **Face Recognition Attendance System** built using **Python, Flask, OpenCV, SQLite, HTML, CSS, and JavaScript**.

This project was developed as my **Final Year Major Project** for the Bachelor of Technology (B.Tech) degree.

The system allows users to **register their face**, recognize them using a webcam, and automatically mark their attendance without any manual work.

---

# 📌 Project Overview

Traditional attendance systems require manual work and consume time.

This project provides a smarter solution by using **Face Recognition Technology**.

The user simply opens the website, registers their face once, and later verifies their identity through the webcam. If the face is recognized successfully, attendance is automatically stored in the database.

The system also prevents duplicate attendance on the same day.

---

# ✨ Features

- 📷 Face Enrollment (Register New User)
- 😊 Face Recognition using Webcam
- ✅ Automatic Attendance Marking
- 🗓️ One Attendance Per Day
- 💾 SQLite Database Storage
- 📊 Attendance Records
- 🌐 Browser-Based Interface
- 📱 Responsive User Interface
- ☁️ Ready for Online Deployment (Render)

---

# 🛠️ Technologies Used

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## Computer Vision

- OpenCV
- LBPH Face Recognizer

## Database

- SQLite

## Deployment

- Gunicorn
- Render

---

# 📂 Project Structure

```
faceattendanceweb1/
│
├── app.py                 # Main Flask Application
├── recognizer.py          # Face Recognition Logic
├── database.py            # Database Initialization
├── attendance.db          # SQLite Database
├── requirements.txt       # Required Python Packages
├── render.yaml            # Render Deployment File
├── Procfile               # Gunicorn Startup File
├── runtime.txt            # Python Runtime Version
├── model.yml              # Trained Face Recognition Model
├── labels.json            # User Labels
│
├── Images/
│      └── User Images
│
├── templates/
│      └── index.html
│
└── static/
       ├── style.css
       └── script.js
```

---

# ⚙️ How the System Works

### Step 1 – Enroll Face

- Open the website.
- Enter your name.
- Start the webcam.
- Capture multiple face images.
- Images are saved inside the **Images** folder.
- The face recognition model is automatically trained.

---

### Step 2 – Verify Face

- Open the Verify section.
- Look at the webcam.
- The system detects your face.
- If recognized successfully, attendance is marked.

---

### Step 3 – Attendance Storage

Attendance is stored inside the SQLite database with:

- Name
- Date
- Time

If attendance has already been marked on the same day, the system will not create another record.

---

# 🗄️ Database

The project uses **SQLite**.

Attendance table contains:

| Field | Description |
|--------|-------------|
| id | Auto Increment ID |
| name | Student Name |
| date | Attendance Date |
| time | Attendance Time |

The system also uses a unique constraint to prevent duplicate attendance on the same day.

---

# 🧠 Face Recognition Process

1. User captures face images.
2. Images are converted into grayscale.
3. Face is detected using OpenCV Haar Cascade.
4. Images are resized and processed.
5. LBPH Face Recognizer is trained.
6. During verification, the captured face is compared with the trained model.
7. If the confidence score is acceptable, attendance is marked.

---

# 🚀 Installation

## Step 1

Clone the repository

```bash
git clone https://github.com/yourusername/face-attendance.git
```

---

## Step 2

Move into the project folder

```bash
cd face-attendance
```

---

## Step 3

Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Step 4

Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5

Run the Application

```bash
python app.py
```

---

## Step 6

Open your browser

```
http://127.0.0.1:5000
```

---

# 📦 Required Python Packages

- Flask
- OpenCV Contrib Python
- NumPy
- Gunicorn

Install all packages using:

```bash
pip install -r requirements.txt
```

---

# 🌐 Deployment

This project is configured for deployment on **Render**.

Deployment files included:

- render.yaml
- Procfile
- runtime.txt

---

# 📈 Future Improvements

Some features that can be added in future:

- Admin Login
- Student Dashboard
- Faculty Dashboard
- Attendance Reports
- Download Attendance as Excel
- Email Notification
- Face Mask Detection
- Anti-Spoofing Detection
- Multi-Face Recognition
- Cloud Database Integration
- Mobile Responsive Improvements

---

# 🎯 Advantages

- Easy to use
- Fast attendance process
- No manual entry
- Reduces human errors
- Saves time
- Browser-based system
- Automatic database management

---

# ⚠️ Limitations

- Good lighting is required.
- Webcam is necessary.
- Works best with clear frontal face images.
- SQLite is suitable for small to medium-sized projects.
- Performance may decrease with a very large number of registered users.

---

# 👨‍💻 Author

**Keshav Kumar**

B.Tech (Artificial Intelligence & Machine Learning)

JB Institute of Technology, Dehradun

Final Year Major Project

---

# 📜 License

This project is developed for **educational and learning purposes**.

You are free to use and modify this project for personal, academic, and research work.

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further improvements.

---

## Thank You 😊
