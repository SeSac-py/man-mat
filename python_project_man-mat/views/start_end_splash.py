from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QTimer, QSize, Qt

class StartEndSplash(QWidget):
    def __init__(self, gif_path, width, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        self.setFixedSize(width, height)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(width, height))
        self.label.setMovie(self.movie)
        self.movie.start()
        QTimer.singleShot(2200, self.goto_next_screen)

    def goto_next_screen(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(1)
