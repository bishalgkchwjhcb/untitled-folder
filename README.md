# QR Code-Based Attendance Management System

A Python-based attendance management system that uses QR codes for tracking student attendance.

## Features

### Student Features
- Personal QR Code Generation
- Download QR Code
- View Attendance History
- View Attendance Percentage

### Admin Features
- Scan Student QR Codes
- Analytics Dashboard
- Department-wise Statistics
- Date Range Filtering
- Student Search and Records

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///attendance.db
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

## Project Structure
```
attendance_system/
├── app.py
├── config.py
├── models/
├── routes/
├── static/
├── templates/
└── utils/
```
