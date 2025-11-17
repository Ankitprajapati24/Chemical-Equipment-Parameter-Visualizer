import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QLabel, QFrame, QTableWidget, QHeaderView, 
                             QLineEdit, QCheckBox, QStatusBar)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QFont, QIcon, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- CONFIGURATION ---
BASE_URL = "http://127.0.0.1:8000/api"

# --- MODERN STYLING (ENHANCED) ---
STYLESHEET = """
    QMainWindow { background-color: #f1f5f9; } /* Slate-100 background */
    QLabel { font-family: 'Segoe UI', sans-serif; color: #334155; }
    
    /* Inputs */
    QLineEdit { 
        padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; background: white;
    }
    QLineEdit:focus { border: 1px solid #3b82f6; }
    
    /* Primary Button (Blue) */
    QPushButton#PrimaryBtn {
        background-color: #3b82f6; color: white; border-radius: 8px;
        padding: 12px 20px; font-weight: 600; border: none; font-size: 14px;
    }
    QPushButton#PrimaryBtn:hover { background-color: #2563eb; }
    QPushButton#PrimaryBtn:pressed { background-color: #1d4ed8; }
    QPushButton#PrimaryBtn:disabled { background-color: #94a3b8; }
    
    /* Secondary Button (Green) */
    QPushButton#SuccessBtn {
        background-color: #10b981; color: white; border-radius: 8px;
        padding: 10px 15px; font-weight: 600; border: none;
    }
    QPushButton#SuccessBtn:hover { background-color: #059669; }
    
    /* Link Button (Text Only) */
    QPushButton#LinkBtn {
        background-color: transparent; color: #3b82f6; border: none; font-weight: 600;
    }
    QPushButton#LinkBtn:hover { text-decoration: underline; color: #2563eb; }

    /* Cards (White Box with Shadow) */
    QFrame#Card { 
        background-color: white; 
        border-radius: 16px; 
        border: 1px solid #e2e8f0;
        /* Note: PyQt doesn't support complex box-shadow in QSS widely, so we use borders/colors */
    }

    /* Checkbox */
    QCheckBox { color: #64748b; spacing: 8px; }
    
    /* Table Styling */
    QTableWidget {
        border: none; background-color: white; gridline-color: #f1f5f9;
    }
    QHeaderView::section {
        background-color: #f8fafc; padding: 10px; border: none; 
        border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #64748b;
    }
    QStatusBar { background: white; border-top: 1px solid #e2e8f0; color: #64748b; }
"""

# --- LOGIN WINDOW ---
class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.is_register_mode = False 
        
        self.setWindowTitle("Login - Chemical Visualizer")
        self.resize(450, 600)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Card
        card = QFrame(); card.setObjectName("Card"); card.setFixedWidth(380)
        self.card_layout = QVBoxLayout(card)
        self.card_layout.setSpacing(15)
        self.card_layout.setContentsMargins(40, 40, 40, 40)

        # Title Icon (Emoji for simplicity)
        self.lbl_icon = QLabel("")
        self.lbl_icon.setStyleSheet("font-size: 48px; margin-bottom: 10px;")
        self.lbl_icon.setAlignment(Qt.AlignCenter)

        # Title Text
        self.lbl_title = QLabel("Welcome Back")
        self.lbl_title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0f172a;")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        
        # Inputs
        self.user_input = QLineEdit(); self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit(); self.pass_input.setPlaceholderText("Password"); self.pass_input.setEchoMode(QLineEdit.Password)
        
        # Confirm Password
        self.confirm_input = QLineEdit(); self.confirm_input.setPlaceholderText("Confirm Password"); self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.hide() 
        
        # Options
        self.chk_show = QCheckBox("Show Password")
        self.chk_show.stateChanged.connect(self.toggle_password_visibility)
        
        # Buttons
        self.btn_action = QPushButton("Log In"); self.btn_action.setObjectName("PrimaryBtn"); self.btn_action.clicked.connect(self.handle_submit)
        self.btn_switch = QPushButton("Create an account"); self.btn_switch.setObjectName("LinkBtn"); self.btn_switch.clicked.connect(self.toggle_mode)

        # Assembly
        self.card_layout.addWidget(self.lbl_icon)
        self.card_layout.addWidget(self.lbl_title)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(QLabel("Username"))
        self.card_layout.addWidget(self.user_input)
        self.card_layout.addWidget(QLabel("Password"))
        self.card_layout.addWidget(self.pass_input)
        self.card_layout.addWidget(self.confirm_input)
        self.card_layout.addWidget(self.chk_show)
        self.card_layout.addSpacing(15)
        self.card_layout.addWidget(self.btn_action)
        self.card_layout.addWidget(self.btn_switch)

        layout.addWidget(card)

    def toggle_password_visibility(self, state):
        mode = QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password
        self.pass_input.setEchoMode(mode)
        self.confirm_input.setEchoMode(mode)

    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        if self.is_register_mode:
            self.lbl_title.setText("Create Account")
            self.btn_action.setText("Sign Up")
            self.btn_switch.setText("Back to Login")
            self.confirm_input.show()
        else:
            self.lbl_title.setText("Welcome Back")
            self.btn_action.setText("Log In")
            self.btn_switch.setText("Create an account")
            self.confirm_input.hide()

    def handle_submit(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        confirm = self.confirm_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Required", "Please fill in all fields")
            return

        if self.is_register_mode:
            if password != confirm:
                QMessageBox.warning(self, "Mismatch", "❌ Passwords do not match!")
                return
            endpoint = f"{BASE_URL}/register/"
        else:
            endpoint = f"{BASE_URL}/login/"
        
        self.btn_action.setEnabled(False)
        self.btn_action.setText("Verifying...")
        QApplication.processEvents()

        try:
            response = requests.post(endpoint, json={"username": username, "password": password})
            self.btn_action.setEnabled(True)
            self.btn_action.setText("Sign Up" if self.is_register_mode else "Log In")

            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                self.on_success(token, username) # SUCCESS!
            else:
                err_msg = response.json().get("error", "Authentication failed")
                # Handle Django validation errors nicely
                if isinstance(response.json(), dict):
                    if 'username' in response.json(): err_msg = response.json()['username'][0]
                QMessageBox.warning(self, "Failed", str(err_msg))
                
        except Exception as e:
            self.btn_action.setEnabled(True)
            self.btn_action.setText("Retry")
            QMessageBox.critical(self, "Connection Error", f"Is the backend running?\n{e}")


# --- DASHBOARD ---
class ModernDashboard(QMainWindow):
    # Signal to tell AppManager to logout
    logout_signal = pyqtSignal()

    def __init__(self, token, username):
        super().__init__()
        self.token = token
        self.current_file_id = None
        
        self.setWindowTitle(f"Dashboard - {username}")
        self.resize(1280, 850)
        self.setStyleSheet(STYLESHEET)

        # Status Bar (New!)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Main Layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(30,30,30,30)
        self.main_layout.setSpacing(20)

        # 1. Header
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl_title = QLabel("Chemical Visualizer")
        lbl_title.setStyleSheet("font-size: 26px; font-weight: 800; color: #0f172a;")
        lbl_subtitle = QLabel("Hybrid Analytics Suite")
        lbl_subtitle.setStyleSheet("font-size: 14px; color: #64748b;")
        title_box.addWidget(lbl_title); title_box.addWidget(lbl_subtitle)
        
        btn_logout = QPushButton("Log Out")
        btn_logout.setStyleSheet("""
            background-color: #fee2e2; color: #ef4444; border: 1px solid #fecaca; 
            border-radius: 6px; padding: 8px 16px; font-weight: bold;
        """)
        btn_logout.clicked.connect(self.logout_signal.emit) # Emit signal instead of close

        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(btn_logout)
        self.main_layout.addLayout(header)

        # 2. Top Section (Upload + Stats)
        top_row = QHBoxLayout()
        
        # Upload Card
        self.upload_card = QFrame(); self.upload_card.setObjectName("Card"); self.upload_card.setFixedWidth(320)
        up_layout = QVBoxLayout(self.upload_card)
        
        self.btn_upload = QPushButton("☁️ Upload CSV File")
        self.btn_upload.setObjectName("PrimaryBtn")
        self.btn_upload.clicked.connect(self.upload_file)
        
        self.lbl_filename = QLabel("No file selected")
        self.lbl_filename.setAlignment(Qt.AlignCenter)
        self.lbl_filename.setStyleSheet("color: #94a3b8; font-style: italic;")
        
        up_layout.addStretch()
        up_layout.addWidget(self.lbl_filename)
        up_layout.addWidget(self.btn_upload)
        up_layout.addStretch()
        
        # Stats Card
        self.stats_card = QFrame(); self.stats_card.setObjectName("Card")
        stats_layout = QHBoxLayout(self.stats_card)
        
        def create_stat(label, val_id):
            w = QWidget()
            l = QVBoxLayout(w)
            t = QLabel(label); t.setStyleSheet("color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: bold;")
            v = QLabel("-"); v.setStyleSheet("font-size: 32px; font-weight: bold; color: #0f172a;")
            setattr(self, val_id, v) # Store reference
            l.addWidget(t); l.addWidget(v); l.setAlignment(Qt.AlignCenter)
            return w
            
        stats_layout.addWidget(create_stat("Total Units", "stat_count"))
        stats_layout.addWidget(create_stat("Avg Temp (°C)", "stat_temp"))
        stats_layout.addWidget(create_stat("Avg Pressure (atm)", "stat_press"))

        top_row.addWidget(self.upload_card)
        top_row.addWidget(self.stats_card)
        self.main_layout.addLayout(top_row)

        # 3. Bottom Section (Graph + Table)
        bot_row = QHBoxLayout()
        
        # Graph Card
        graph_card = QFrame(); graph_card.setObjectName("Card")
        self.chart_layout = QVBoxLayout(graph_card)
        lbl_graph = QLabel("📊 Equipment Distribution"); lbl_graph.setStyleSheet("font-size: 16px; font-weight: 700; margin-bottom: 10px;")
        self.chart_layout.addWidget(lbl_graph)
        bot_row.addWidget(graph_card, stretch=4)
        
        # Table Card
        table_card = QFrame(); table_card.setObjectName("Card")
        tab_layout = QVBoxLayout(table_card)
        
        tab_header = QHBoxLayout()
        lbl_tab = QLabel("📝 Live Data"); lbl_tab.setStyleSheet("font-size: 16px; font-weight: 700;")
        
        self.btn_pdf = QPushButton("Download PDF")
        self.btn_pdf.setObjectName("SuccessBtn")
        self.btn_pdf.setEnabled(False)
        self.btn_pdf.clicked.connect(self.download_pdf)
        
        tab_header.addWidget(lbl_tab); tab_header.addStretch(); tab_header.addWidget(self.btn_pdf)
        tab_layout.addLayout(tab_header)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True) # NEW: Enable Sorting!
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab_layout.addWidget(self.table)
        
        bot_row.addWidget(table_card, stretch=6)
        self.main_layout.addLayout(bot_row, stretch=1)

        self.show()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.lbl_filename.setText(file_path.split("/")[-1])
            self.status_bar.showMessage("Uploading and Analyzing...")
            self.btn_upload.setEnabled(False)
            self.btn_upload.setText("Processing...")
            QApplication.processEvents()
            
            files = {'file': open(file_path, 'rb')}
            headers = {'Authorization': f'Token {self.token}'}
            
            try:
                response = requests.post(f"{BASE_URL}/analyze/", files=files, headers=headers)
                
                self.btn_upload.setEnabled(True)
                self.btn_upload.setText("☁️ Upload CSV File")

                if response.status_code == 200:
                    self.status_bar.showMessage("Analysis Complete", 5000)
                    self.display_results(response.json())
                else:
                    self.status_bar.showMessage("Upload Failed")
                    QMessageBox.critical(self, "Error", f"Server failed: {response.text}")
            except Exception as e:
                self.btn_upload.setEnabled(True)
                self.status_bar.showMessage("Connection Error")
                QMessageBox.critical(self, "Error", str(e))

    def display_results(self, data):
        # Stats
        self.stat_count.setText(str(data.get('total_equipment_count', 0)))
        self.stat_temp.setText(f"{data.get('average_temperature', 0):.1f}")
        self.stat_press.setText(f"{data.get('average_pressure', 0):.1f}")
        
        self.current_file_id = data.get("id")
        if self.current_file_id: self.btn_pdf.setEnabled(True)
        
        # Table
        rows = data.get("preview", [])
        if rows:
            cols = list(rows[0].keys())
            self.table.setColumnCount(len(cols)); self.table.setHorizontalHeaderLabels(cols)
            self.table.setRowCount(len(rows))
            self.table.setSortingEnabled(False) # Disable sorting while populating
            for r, row in enumerate(rows):
                for c, h in enumerate(cols):
                    item = QTableWidgetItem(str(row.get(h, "")))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(r, c, item)
            self.table.setSortingEnabled(True) # Re-enable sorting

        # Chart
        for i in reversed(range(self.chart_layout.count())): 
            if i > 0: self.chart_layout.itemAt(i).widget().setParent(None)
            
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)
        
        ax = canvas.figure.subplots()
        types = data.get("type_counts", {})
        names = list(types.keys())
        values = list(types.values())
        
        bars = ax.bar(names, values, color='#3b82f6', zorder=3)
        
        # NEW: Add labels on top of bars
        try:
            ax.bar_label(bars, padding=3) 
        except: pass # Fallback for old matplotlib versions
        
        ax.set_facecolor("white")
        ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False); ax.spines['bottom'].set_color('#cbd5e1')
        canvas.draw()

    def download_pdf(self):
        if self.current_file_id:
            QDesktopServices.openUrl(QUrl(f"{BASE_URL}/report/{self.current_file_id}/"))


# --- APP MANAGER (Controls flow) ---
class AppManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setFont(QFont("Segoe UI", 10))
        
        self.login_window = None
        self.dashboard = None
        
        self.show_login()
        sys.exit(self.app.exec_())

    def show_login(self):
        self.login_window = LoginWindow(self.show_dashboard)
        self.login_window.show()
        if self.dashboard: 
            self.dashboard.close()
            self.dashboard = None

    def show_dashboard(self, token, username):
        self.dashboard = ModernDashboard(token, username)
        # Connect the logout signal to the show_login function
        self.dashboard.logout_signal.connect(self.show_login)
        self.dashboard.show()
        self.login_window.close()

if __name__ == "__main__":
    AppManager()