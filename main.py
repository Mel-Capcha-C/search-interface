from PySide6.QtWidgets import QApplication
from my_library import RGMainWindow
import qdarkstyle
from qdarkstyle.light.palette import LightPalette
import sys

app = QApplication(sys.argv)
# stylesheet = qdarkstyle.load_stylesheet(palette=LightPalette)
# app.setStyleSheet(stylesheet)
window = RGMainWindow(app)
window.show()
app.exec()
