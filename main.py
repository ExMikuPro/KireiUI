import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KireiUI")
        self.resize(900, 600)

        label = QLabel("Hello KireiUI")
        label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 600;
                color: #1f2937;
                qproperty-alignment: AlignCenter;
            }
        """)

        self.setCentralWidget(label)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()