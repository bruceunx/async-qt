import sys
import time
import asyncio
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class Worker(QThread):
    info = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.signal = True

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.loop())
        loop.run_until_complete(task)

    async def loop(self) -> None:
        while self.signal:
            await asyncio.sleep(1)
            self.info.emit(str(time.time()))
        print("close")

    @Slot()
    def _stop(self) -> None:
        self.signal = False


class Window(QWidget):

    closeThread = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 500, 200)
        self.show()
        self.setLayout(QVBoxLayout())

        self.label = QLabel('Hello')

        self.layout().addWidget(self.label)
        self.worker = Worker()
        self.worker.info.connect(self.label.setText)
        self.closeThread.connect(self.worker._stop)

        self.worker.start()

    def closeEvent(self, closeEvent: QCloseEvent) -> None:

        self.closeThread.emit()
        time.sleep(1)
        self.worker.quit()

        super().closeEvent(closeEvent)


app = QApplication()
win = Window()

sys.exit(app.exec())
