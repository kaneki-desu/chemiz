from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTableWidget, QTableWidgetItem


class TablePanel(QGroupBox):
    def __init__(self):
        super().__init__("Equipment Type Table")
        self.setCheckable(True)
        self.setChecked(True)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

    def update_table(self, summary):
        dist = summary.get("type_distribution", {})

        self.table.setRowCount(len(dist))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Equipment Type", "Count"])

        for i, (key, val) in enumerate(dist.items()):
            self.table.setItem(i, 0, QTableWidgetItem(key))
            self.table.setItem(i, 1, QTableWidgetItem(str(val)))
