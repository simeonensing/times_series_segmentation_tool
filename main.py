import sys
from PyQt5.QtWidgets import QApplication
from utils.ts_segmentaion_class import ts_segmentation_GUI

def main():
    """Main GUI application."""
    app = QApplication(sys.argv)
    window = ts_segmentation_GUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

