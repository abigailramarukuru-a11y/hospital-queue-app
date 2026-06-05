# Hospital Queue Management System

## Overview

The Hospital Queue Management System is a web-based application developed using Python, Flask, SQLite, HTML, and Bootstrap.

The purpose of the system is to reduce long hospital queues by allowing patients to book appointments and join a queue digitally. Hospital staff can view, search, edit, and manage patients in the queue.

This project was developed as a learning project and is currently a working prototype. Additional features and improvements are planned for future versions.

---

## Features

* Add new patients to the queue
* View all patients currently in the queue
* Search for patients by name
* Edit patient information
* Serve patients and remove them from the queue
* Department-based queue management
* Simple and user-friendly web interface

---

## Technologies Used

* Python 3
* Flask
* SQLite3
* HTML5
* Bootstrap 5
* Git & GitHub

---

## Project Structure

```text
hospital-queue-app/
│
├── app.py
├── hospital.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── home.html
│   ├── queue.html
│   ├── search.html
│   ├── edit.html
│   └── ...
│
└── static/
```

---

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/abigailramarukuru-a11y/hospital-queue-app.git
```

Move into the project folder:

```bash
cd hospital-queue-app
```

---

### Step 2: Create a Virtual Environment

Linux/Mac:

```bash
python3 -m venv venv
```

Windows:

```bash
python -m venv venv
```

---

### Step 3: Activate the Virtual Environment

Linux/Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

After activation you should see:

```text
(venv)
```

at the beginning of your terminal prompt.

---

### Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

---

### Step 5: Run the Application

```bash
python3 app.py
```

or

```bash
python app.py
```

You should see output similar to:

```text
* Running on http://127.0.0.1:5000
```

---

### Step 6: Open the Application

Open your web browser and visit:

```text
http://127.0.0.1:5000
```

The Hospital Queue Management System should now be running.

---

## Troubleshooting

### ModuleNotFoundError

Install dependencies again:

```bash
pip install -r requirements.txt
```

### Port Already in Use

Stop the application using:

```bash
CTRL + C
```

Then run it again.

### Database Errors

Ensure that the file:

```text
hospital.db
```

exists in the project directory.

---

## Future Improvements

Planned features include:

* User authentication and login
* Admin dashboard
* Appointment scheduling
* SMS or email notifications
* Better security controls
* Improved user interface
* Reporting and analytics

---

## Author

Abigail Ogone Ramarukuru

Bachelor of Science in Network Security and Computer Forensics

Botho University

Botswana

GitHub: https://github.com/abigailramarukuru-a11y

