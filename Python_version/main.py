import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow
import nltk

def initialize_nltk():
    try:
        # Download all required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)  # commonly needed
        
        # Verify the downloads by trying to load stopwords
        from nltk.corpus import stopwords
        stopwords.words('english')
        
    except Exception as e:
        raise RuntimeError(f"Failed to initialize NLTK data: {str(e)}")

def main():
    try:
        # Initialize NLTK before starting the application
        initialize_nltk()
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        # Handle errors
        if QApplication.instance():
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
        else:
            print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 