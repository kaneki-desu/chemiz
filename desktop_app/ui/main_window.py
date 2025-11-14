from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QSplitter
from PyQt5.QtCore import Qt

from backend.api import upload_csv, fetch_history, download_pdf

from ui.summary_panel import SummaryPanel
from ui.table_panel import TablePanel
from ui.chart_panel import ChartPanel
from ui.history_panel import HistoryPanel


class ChemicalVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(950, 750)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Buttons ---
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_action)

        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.clicked.connect(self.download_pdf_action)
        self.pdf_btn.setEnabled(False)

        layout.addWidget(self.upload_btn)
        layout.addWidget(self.pdf_btn)

        # --- Splitter + Panels ---
        self.splitter = QSplitter(Qt.Vertical)
        layout.addWidget(self.splitter)

        self.summary_panel = SummaryPanel()
        self.table_panel = TablePanel()
        self.chart_panel = ChartPanel()
        self.history_panel = HistoryPanel(self.load_dataset_from_history)

        self.splitter.addWidget(self.summary_panel)
        self.splitter.addWidget(self.table_panel)
        self.splitter.addWidget(self.chart_panel)
        self.splitter.addWidget(self.history_panel)

        # State
        self.current_summary = None
        self.last_dataset_id = None

        self.refresh_history()

    # ------------------------------------------------------
    # Upload CSV
    def upload_action(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        res = upload_csv(file_path)
        if res.status_code not in (200, 201):
            QMessageBox.critical(self, "Upload Error", res.text)
            return

        data = res.json()
        self.last_dataset_id = data.get("id")
        summary = data.get("summary", {})

        self.update_panels(summary)
        self.refresh_history()

    # ------------------------------------------------------
    # Update All Panels Together
    def update_panels(self, summary):
        self.current_summary = summary
        self.summary_panel.update_summary(summary)
        self.table_panel.update_table(summary)
        self.chart_panel.update_chart(summary)
        self.pdf_btn.setEnabled(True)

    # ------------------------------------------------------
    # PDF Download
    def download_pdf_action(self):
        if not self.last_dataset_id:
            QMessageBox.warning(self, "No Dataset", "Nothing to download.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "equipment_report.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        res = download_pdf(self.last_dataset_id)
        if res.status_code != 200:
            QMessageBox.critical(self, "Download Error", res.text)
            return

        with open(file_path, "wb") as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)

        QMessageBox.information(self, "Saved", "PDF Saved Successfully!")

    # ------------------------------------------------------
    # Load history list from server
    def refresh_history(self):
        res = fetch_history()
        if res.status_code == 200:
            self.history_panel.update_history(res.json())

    # ------------------------------------------------------
    # When user clicks an item in history
    def load_dataset_from_history(self, dataset):
        self.last_dataset_id = dataset["id"]
        summary = dataset.get("summary", {})
        self.update_panels(summary)
