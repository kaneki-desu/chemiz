import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
    QListWidget, QGroupBox, QSplitter
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Backend endpoints
API_UPLOAD = "https://chemiz.onrender.com/api/upload/"
API_HISTORY = "https://chemiz.onrender.com/api/history/"
API_DOWNLOAD = "https://chemiz.onrender.com/api/download/"

# Authentication
AUTH_CREDENTIALS = ("sibaj", "12345678")


class ChemicalVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(900, 700)

        main_layout = QVBoxLayout()

        # Upload & PDF buttons
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setEnabled(False)
        main_layout.addWidget(self.upload_btn)
        main_layout.addWidget(self.pdf_btn)

        # Splitter for resizable sections
        self.splitter = QSplitter(Qt.Vertical)

        # ===== Summary Section =====
        self.summary_group = QGroupBox("Summary")
        self.summary_group.setCheckable(True)
        self.summary_group.setChecked(True)
        summary_layout = QVBoxLayout()
        self.summary_label = QLabel("Upload a CSV to view summary")
        summary_layout.addWidget(self.summary_label)
        self.summary_group.setLayout(summary_layout)
        self.splitter.addWidget(self.summary_group)

        # ===== Table Section =====
        self.table_group = QGroupBox("Equipment Type Table")
        self.table_group.setCheckable(True)
        self.table_group.setChecked(True)
        table_layout = QVBoxLayout()
        self.table = QTableWidget()
        table_layout.addWidget(self.table)
        self.table_group.setLayout(table_layout)
        self.splitter.addWidget(self.table_group)

        # ===== Chart Section =====
        self.chart_group = QGroupBox("Equipment Type Charts")
        self.chart_group.setCheckable(True)
        self.chart_group.setChecked(True)
        chart_layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(6, 3)))
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)
        self.splitter.addWidget(self.chart_group)

        # ===== History Section =====
        self.history_group = QGroupBox("Last 5 Uploaded Datasets")
        self.history_group.setCheckable(True)
        self.history_group.setChecked(True)
        history_layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.select_dataset)
        history_layout.addWidget(self.history_list)
        self.history_group.setLayout(history_layout)
        self.splitter.addWidget(self.history_group)

        # Add splitter to main layout
        main_layout.addWidget(self.splitter)

        self.setLayout(main_layout)
        self.current_summary = None
        self.last_dataset_id = None
        self.history_data = []

        # Fetch history on startup
        self.fetch_history()

    # ---------------- Backend methods ----------------
    def fetch_history(self):
        try:
            res = requests.get(API_HISTORY, auth=AUTH_CREDENTIALS)
            if res.status_code == 200:
                self.history_data = res.json()
                self.history_list.clear()
                for d in self.history_data:
                    self.history_list.addItem(f"ID: {d['id']} | Uploaded: {d['uploaded_at']}")
            else:
                QMessageBox.warning(self, "Error", "Could not fetch history")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"History fetch failed: {e}")

    def select_dataset(self, item):
        index = self.history_list.row(item)
        dataset = self.history_data[index]
        self.last_dataset_id = dataset['id']
        self.current_summary = dataset.get('summary', {})
        self.show_summary(self.current_summary)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                res = requests.post(API_UPLOAD, files={"file": f}, auth=AUTH_CREDENTIALS)

            if res.status_code not in (200, 201):
                QMessageBox.critical(self, "Error", f"Upload failed: {res.text}")
                return

            data = res.json()
            self.last_dataset_id = data.get("id")
            self.current_summary = data.get("summary", data)
            self.show_summary(self.current_summary)
            self.fetch_history()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong: {e}")

    def show_summary(self, summary):
        if not summary:
            QMessageBox.warning(self, "Empty", "No summary data found")
            return

        total = summary.get("total_equipment", 0)
        flow = summary.get("average_flowrate", 0)
        pressure = summary.get("average_pressure", 0)
        temp = summary.get("average_temperature", 0)

        text = (
            f"Total Equipments: {total}\n"
            f"Average Flowrate: {flow:.2f}\n"
            f"Average Pressure: {pressure:.2f}\n"
            f"Average Temperature: {temp:.2f}"
        )
        self.summary_label.setText(text)

        # Table
        dist = summary.get("type_distribution", {})
        self.table.setRowCount(len(dist))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Equipment Type", "Count"])
        for i, (key, val) in enumerate(dist.items()):
            self.table.setItem(i, 0, QTableWidgetItem(key))
            self.table.setItem(i, 1, QTableWidgetItem(str(val)))

        # Charts
        self.canvas.figure.clear()
        ax1 = self.canvas.figure.add_subplot(121)
        ax2 = self.canvas.figure.add_subplot(122)
        ax1.bar(dist.keys(), dist.values(), color="skyblue")
        ax1.set_title("Equipment Type Distribution (Bar)")
        ax2.pie(dist.values(), labels=dist.keys(), autopct="%1.1f%%", startangle=90)
        ax2.set_title("Equipment Type Distribution (Pie)")
        self.canvas.draw()

        self.pdf_btn.setEnabled(True)

    def download_pdf(self):
        if not self.last_dataset_id:
            QMessageBox.warning(self, "No dataset", "Please select a dataset to download.")
            return
        try:
            url = f"{API_DOWNLOAD}?id={self.last_dataset_id}"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", "equipment_summary.pdf", "PDF Files (*.pdf)")
            if not file_path:
                return

            res = requests.get(url, auth=AUTH_CREDENTIALS, stream=True)
            if res.status_code != 200:
                QMessageBox.critical(self, "Error", f"Download failed: {res.text}")
                return

            with open(file_path, "wb") as f:
                for chunk in res.iter_content(1024):
                    f.write(chunk)

            QMessageBox.information(self, "PDF saved", f"PDF saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"PDF download failed: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChemicalVisualizer()
    window.show()
    sys.exit(app.exec_())
