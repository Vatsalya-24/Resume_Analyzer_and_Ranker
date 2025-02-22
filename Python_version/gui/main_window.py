from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QFileDialog, QTextEdit, QLabel, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSlot, QThread
from .resume_table import ResumeTable
from processors.resume_processor import ResumeProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Resume Analyzer & Ranker")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.resume_processor = ResumeProcessor()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Job Requirements Input
        self.req_label = QLabel("Enter Job Requirements:")
        self.req_text = QTextEdit()
        
        # Buttons
        self.load_btn = QPushButton("Load Resumes")
        self.analyze_btn = QPushButton("Analyze Resumes")
        self.analyze_btn.setEnabled(False)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        
        # Results Table
        self.results_table = ResumeTable()
        
        # Add widgets to layout
        layout.addWidget(self.req_label)
        layout.addWidget(self.req_text)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.analyze_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.results_table)
        
        # Connect signals
        self.load_btn.clicked.connect(self.load_resumes)
        self.analyze_btn.clicked.connect(self.analyze_resumes)
        
    @pyqtSlot()
    def load_resumes(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Resumes",
            "",
            "Documents (*.pdf *.docx)"
        )
        if files:
            self.resume_processor.set_files(files)
            self.analyze_btn.setEnabled(True)
    
    @pyqtSlot()
    def analyze_resumes(self):
        requirements = self.req_text.toPlainText()
        if not requirements:
            return
            
        self.progress_bar.setRange(0, 0)  # Show indefinite progress
        self.analyze_btn.setEnabled(False)
        
        # Start processing in a separate thread
        self.worker_thread = QThread()
        self.resume_processor.moveToThread(self.worker_thread)
        self.resume_processor.analysis_complete.connect(self.update_results)
        self.worker_thread.started.connect(
            lambda: self.resume_processor.process_resumes(requirements)
        )
        self.worker_thread.start()
    
    @pyqtSlot(list)
    def update_results(self, results):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.analyze_btn.setEnabled(True)
        self.results_table.update_results(results)
        self.worker_thread.quit() 