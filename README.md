# ⚗️ Chemical Equipment Parameter Visualizer

A Hybrid Application (Web + Desktop) for visualizing and analyzing chemical equipment data. Built with **Django**, **React**, and **PyQt5**.

## 🚀 Key Features
* **Hybrid Architecture:** Single Django Backend serving both Web (React) and Desktop (PyQt5) frontends.
* **Data Analytics:** Upload CSV files to calculate Average Temperature, Pressure, and Flow Rates.
* **Visualization:** Interactive Charts (Chart.js & Matplotlib) and Data Tables.
* **Reporting:** Auto-generated PDF Reports.
* **Security:** Token-based Authentication (Login/Register) system.
* **History:** Tracks the last 5 uploaded datasets.

## 🛠️ Tech Stack
* **Backend:** Python Django + Django REST Framework + SQLite
* **Data Processing:** Pandas
* **Web Frontend:** React.js + Chart.js + Axios
* **Desktop Frontend:** PyQt5 + Matplotlib

---

## ⚙️ Setup Instructions

### 1. Backend (Django)
The brain of the application. Must be running for frontends to work.

```bash
# Navigate to backend folder
cd chemical_project

# Install dependencies
pip install -r requirements.txt

# Setup Database
python manage.py migrate

# Start Server
python manage.py runserver