import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QLabel, QFrame, QTableWidget, QHeaderView, QSizePolicy)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QFont, QColor, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api/analyze/"

# --- MODERN STYLING (QSS) ---
STYLESHEET = """
    QMainWindow {
        background-color: #f8fafc;
    }
    QLabel {
        font-family: 'Segoe UI', sans-serif;
        color: #1e293b;
    }
    /* Cards */
    QFrame#Card {
        background-color: white;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
    }
    /* Headers */
    QLabel#Header {
        font-size: 24px;
        font-weight: bold;
        color: #0f172a;
    }
    QLabel#SubHeader {
        font-size: 16px;
        font-weight: bold;
        color: #64748b;
        margin-bottom: 10px;
    }
    /* Stats */
    QLabel#StatValue {
        font-size: 28px;
        font-weight: bold;
        color: #3b82f6;
    }
    QLabel#StatLabel {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Buttons */
    QPushButton {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2563eb;
    }
    QPushButton:pressed {
        background-color: #1d4ed8;
    }
    QPushButton:disabled {
        background-color: #cbd5e1;
    }
    /* Secondary Button (PDF) */
    QPushButton#SecondaryBtn {
        background-color: #10b981;
    }
    QPushButton#SecondaryBtn:hover {
        background-color: #059669;
    }
    /* Table */
    QTableWidget {
        border: none;
        background-color: white;
        gridline-color: #f1f5f9;
    }
    QHeaderView::section {
        background-color: #f8fafc;
        padding: 8px;
        border: none;
        border-bottom: 2px solid #e2e8f0;
        font-weight: bold;
        color: #64748b;
    }
"""

class ModernDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" 🧪 Chemical Equipment Parameter Visualizer - Desktop App")
        self.resize(1200, 800)
        self.setStyleSheet(STYLESHEET)

        # Main Container
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 1. Header Section
        header_layout = QHBoxLayout()
        title = QLabel("🧪 Chemical Equipment Parameter Visualizer")
        title.setObjectName("Header")
        header_layout.addWidget(title)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # 2. Top Row: Upload + Stats
        top_row = QHBoxLayout()
        self.main_layout.addLayout(top_row)

        # -- Upload Card --
        self.upload_card = QFrame()
        self.upload_card.setObjectName("Card")
        self.upload_card.setFixedWidth(300)
        upload_layout = QVBoxLayout(self.upload_card)
        
        self.lbl_status = QLabel("No file selected")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        
        self.btn_upload = QPushButton("☁️ Select CSV File")
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.upload_file)
        
        upload_layout.addStretch()
        upload_layout.addWidget(self.lbl_status)
        upload_layout.addWidget(self.btn_upload)
        upload_layout.addStretch()
        
        top_row.addWidget(self.upload_card)

        # -- Stats Card (Grid of 3 items) --
        self.stats_card = QFrame()
        self.stats_card.setObjectName("Card")
        stats_layout = QHBoxLayout(self.stats_card)
        
        # Helper to create stat block
        def create_stat(label, value_id):
            container = QWidget()
            layout = QVBoxLayout(container)
            lbl_title = QLabel(label)
            lbl_title.setObjectName("StatLabel")
            lbl_val = QLabel("-")
            lbl_val.setObjectName("StatValue")
            setattr(self, value_id, lbl_val) # Save reference to update later
            layout.addWidget(lbl_title)
            layout.addWidget(lbl_val)
            layout.setAlignment(Qt.AlignCenter)
            return container

        stats_layout.addWidget(create_stat("TOTAL UNITS", "val_count"))
        stats_layout.addWidget(create_stat("AVG TEMP (°C)", "val_temp"))
        stats_layout.addWidget(create_stat("AVG PRESSURE", "val_press"))
        
        top_row.addWidget(self.stats_card)

        # 3. Bottom Row: Graph + Table
        bottom_row = QHBoxLayout()
        self.main_layout.addLayout(bottom_row, stretch=1)

        # -- Graph Card --
        graph_card = QFrame()
        graph_card.setObjectName("Card")
        self.graph_layout = QVBoxLayout(graph_card)
        
        graph_header = QLabel("📊 Distribution")
        graph_header.setObjectName("SubHeader")
        self.graph_layout.addWidget(graph_header)
        
        # Placeholder for the chart
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        self.graph_layout.addWidget(self.chart_container)
        
        bottom_row.addWidget(graph_card, stretch=4) # 40% width

        # -- Table Card --
        table_card = QFrame()
        table_card.setObjectName("Card")
        table_layout = QVBoxLayout(table_card)
        
        # Header with PDF Button
        table_header_row = QHBoxLayout()
        lbl_table = QLabel("📝 Recent Data")
        lbl_table.setObjectName("SubHeader")
        
        self.btn_pdf = QPushButton("Download Report")
        self.btn_pdf.setObjectName("SecondaryBtn")
        self.btn_pdf.setCursor(Qt.PointingHandCursor)
        self.btn_pdf.setEnabled(False)
        self.btn_pdf.clicked.connect(self.download_pdf)
        
        table_header_row.addWidget(lbl_table)
        table_header_row.addStretch()
        table_header_row.addWidget(self.btn_pdf)
        
        table_layout.addLayout(table_header_row)

        # The Table Widget
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True) # Zebra striping
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.table)
        
        bottom_row.addWidget(table_card, stretch=6) # 60% width

        # Internal Data State
        self.current_file_id = None
        self.show()

    # --- LOGIC FUNCTIONS (Same as before) ---

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.lbl_status.setText(file_path.split("/")[-1]) # Show filename
            files = {'file': open(file_path, 'rb')}
            try:
                # Change button text to show loading
                self.btn_upload.setText("Processing...")
                self.btn_upload.setEnabled(False)
                QApplication.processEvents() # Force UI update

                response = requests.post(API_URL, files=files)
                
                self.btn_upload.setText("☁️ Select CSV File")
                self.btn_upload.setEnabled(True)

                if response.status_code == 200:
                    self.display_results(response.json())
                else:
                    QMessageBox.critical(self, "Error", f"Server failed: {response.text}")
            except Exception as e:
                self.btn_upload.setText("Retry Upload")
                self.btn_upload.setEnabled(True)
                QMessageBox.critical(self, "Connection Error", f"Could not connect.\n{str(e)}")

    def display_results(self, data):
        # 1. Update Stats
        self.val_count.setText(str(data.get('total_equipment_count', 0)))
        self.val_temp.setText(f"{data.get('average_temperature', 0):.1f}")
        self.val_press.setText(f"{data.get('average_pressure', 0):.1f}")

        # 2. Handle PDF Button
        self.current_file_id = data.get("id")
        if self.current_file_id:
            self.btn_pdf.setText(f"📄 PDF Report")
            self.btn_pdf.setEnabled(True)

        # 3. Fill Table
        rows = data.get("preview", [])
        if rows:
            columns = list(rows[0].keys())
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, header in enumerate(columns):
                    item = QTableWidgetItem(str(row_data.get(header, "")))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)

        # 4. Plot Graph
        self.plot_data(data.get("type_counts", {}))

    def plot_data(self, type_counts):
        # Clear previous chart
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)

        # Create new Matplotlib Figure
        # Note: We use 'facecolor' to match the container background if needed, or white
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)
        
        ax = canvas.figure.subplots()
        names = list(type_counts.keys())
        values = list(type_counts.values())
        
        # Modern Bar Style
        bars = ax.bar(names, values, color='#3b82f6', zorder=3)
        
        # Styling the Axes to look like Chart.js
        ax.set_facecolor("white")
        ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#cbd5e1')
        
        canvas.draw()

    def download_pdf(self):
        if self.current_file_id:
            url = f"http://127.0.0.1:8000/api/report/{self.current_file_id}/"
            QDesktopServices.openUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set a global font for the whole app
    app.setFont(QFont("Segoe UI", 10))
    window = ModernDashboard()
    sys.exit(app.exec_())