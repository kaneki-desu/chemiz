from PyQt5.QtWidgets import QGroupBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from utils.plot_helpers import draw_equipment_charts


class ChartPanel(QGroupBox):
    def __init__(self):
        super().__init__("Equipment Type Charts")
        self.setCheckable(True)
        self.setChecked(True)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(6, 3)))
        layout.addWidget(self.canvas)

    def update_chart(self, summary):
        draw_equipment_charts(self.canvas, summary)
