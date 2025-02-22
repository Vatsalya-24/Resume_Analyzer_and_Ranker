from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

class ResumeTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_table()
        
    def setup_table(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels([
            "Rank",
            "Name",
            "Match Score",
            "Key Skills",
            "Experience"
        ])
        self.horizontalHeader().setStretchLastSection(True)
        
    def update_results(self, results):
        self.setRowCount(len(results))
        for i, result in enumerate(results):
            self.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.setItem(i, 1, QTableWidgetItem(result['name']))
            self.setItem(i, 2, QTableWidgetItem(f"{result['score']:.2f}%"))
            self.setItem(i, 3, QTableWidgetItem(", ".join(result['skills'])))
            self.setItem(i, 4, QTableWidgetItem(str(result['experience']))) 