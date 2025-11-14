from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel


class SummaryPanel(QGroupBox):
    def __init__(self):
        super().__init__("Summary")
        self.setCheckable(True)
        self.setChecked(True)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Upload a CSV to view summary")
        layout.addWidget(self.label)

    def update_summary(self, summary):
        if not summary:
            self.label.setText("No summary available")
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
        self.label.setText(text)
