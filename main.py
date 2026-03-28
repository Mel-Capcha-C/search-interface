from PySide6.QtWidgets import QApplication
from my_library import RGMainWindow
import sys

app = QApplication(sys.argv)
window = RGMainWindow(app)
window.show()
app.exec()
