from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QListWidget


class HistoryPanel(QGroupBox):
    def __init__(self, on_select_callback):
        super().__init__("Last 5 Uploaded Datasets")
        self.setCheckable(True)
        self.setChecked(True)

        self.on_select_callback = on_select_callback

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.list = QListWidget()
        self.list.itemClicked.connect(self._item_clicked)
        layout.addWidget(self.list)

        self.history_data = []

    def update_history(self, history):
        self.history_data = history
        self.list.clear()

        for d in history:
            txt = f"ID: {d['id']} | Uploaded: {d['uploaded_at']}"
            self.list.addItem(txt)

    def _item_clicked(self, item):
        index = self.list.row(item)
        dataset = self.history_data[index]
        self.on_select_callback(dataset)
