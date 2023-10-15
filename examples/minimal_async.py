import asyncio
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget)

from utils import AsyncHelper


class MainWindow(QMainWindow):

    start_signal = Signal()
    done_signal = Signal()

    start_signal1 = Signal()
    done_signal1 = Signal()

    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

        self.text = QLabel("The answer is 42.")
        layout.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)

        async_trigger = QPushButton(text="What is the question?")
        async_trigger.clicked.connect(lambda: self.start_signal.emit())
        layout.addWidget(async_trigger, alignment=Qt.AlignmentFlag.AlignCenter)

        async_trigger1 = QPushButton(text="pushButton1")
        async_trigger1.clicked.connect(lambda: self.start_signal1.emit())
        layout.addWidget(async_trigger1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.helps = []

        self.helps.append(
            AsyncHelper(self, self.set_text, "start_signal", "done_signal"))
        self.helps.append(
            AsyncHelper(self, self.set_text1, "start_signal1", "done_signal1"))

    async def set_text(self):
        await asyncio.sleep(1)
        self.text.setText("What do you get if you multiply six by nine?")
        self.done_signal.emit()

    async def set_text1(self):
        await asyncio.sleep(1)
        self.text.setText("add another async function")
        await asyncio.sleep(10)
        self.done_signal1.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
