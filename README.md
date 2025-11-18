# ⚗️ Chemical Equipment Parameter Visualizer

A full-stack **Hybrid Application** (Web + Desktop) for visualizing and analyzing chemical equipment data. Built with **Django**, **React**, and **PyQt5**, demonstrating a shared backend architecture across multiple platforms.

> **Intern Screening Task Submission**

---

## 🚀 Live Demo
* **Web Dashboard:** [INSERT_YOUR_RENDER_STATIC_SITE_URL_HERE]
* **Backend API:** [INSERT_YOUR_RENDER_BACKEND_URL_HERE]

*(Note: The Desktop Application can connect to either the Live API or a Local Server).*

---

## 📺 Demo Video
Watch the full application walkthrough demonstrating the Hybrid Architecture:

[![Watch the Demo](https://drive.google.com/file/d/1kW7xog2vgrURjSVpczQAo_86VIXuIb0c/view?usp=drive_link)

*(Click the image above to watch the video)*

---

## 📸 Screenshots

### 1. Web Dashboard (React)
*Modern glassmorphism interface with interactive Chart.js analytics and data tables.*
![Web Dashboard](screenshots/web.png)

### 2. Desktop Application (PyQt5)
*Native desktop experience connecting to the same cloud backend via REST API.*
![Desktop App](screenshots/desktop.png)

### 3. PDF Analysis Report
*Auto-generated downloadable report with embedded analytics using ReportLab.*
![PDF Report](screenshots/pdf.png)

---

## 🌟 Key Features
* **Hybrid Architecture:** A single **Django REST Framework** API serving both a React Web App and a PyQt5 Desktop App simultaneously.
* **Data Analytics:** Automated **Pandas** processing of CSV uploads to calculate Average Temperature, Pressure, and Flow Rates.
* **Visualization:**
    * **Web:** Interactive bar charts using **Chart.js**.
    * **Desktop:** Embedded **Matplotlib** graphs within the PyQt5 window.
* **Reporting:** Auto-generated **PDF Reports** with summary statistics.
* **Security:** **Token-based Authentication** (Login/Register) with secure password hashing.
* **History Management:** Database tracks and stores the last 5 uploaded datasets per user.
* **Modern UI:** Consistent "Blue/White" design language across both platforms.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python Django + DRF | API & Business Logic |
| **Database** | SQLite (Dev) / Postgres (Prod) | Data Storage |
| **Data Processing** | Pandas | CSV Parsing & Statistics |
| **Web Frontend** | React.js + Chart.js + Axios | Browser Interface |
| **Desktop Frontend** | Python PyQt5 + Matplotlib | Native OS Interface |
| **Deployment** | Docker + Render | Cloud Hosting |

---

## 📂 Project Structure

```bash
├── chemical_project/       # Django Backend
│   ├── api/                # API Logic (Views, Serializers, Models)
│   ├── Dockerfile          # Cloud Build Configuration
│   ├── requirements.txt    # Python Dependencies
│   └── manage.py
├── web-frontend/           # React Web Application
│   ├── src/                # React Components (LoginScreen, Dashboard)
│   └── package.json
├── main.py                 # Desktop Application Entry Point (PyQt5)
├── docker-compose.yml      # Local Docker Orchestration
├── sample_equipment_data.csv # Test Data
└── README.md               # Documentation

## ⚙️ Installation & Run Instructions

You can run this project using **Docker** (Recommended) or **Manually**.

### Option A: Docker (Fastest)
If you have Docker installed, you can launch the Backend and Web App instantly.

1.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```
2.  **Access:**
    * **Web App:** `http://localhost:3000`
    * **Backend:** `http://localhost:8000`

### Option B: Manual Setup

#### 1. Backend (Django)
```bash
# Navigate to backend folder
cd chemical_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate

# Start Server
python manage.py runserver
