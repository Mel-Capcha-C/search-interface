"""Example 1: Basic PySide6 Application with a Button
from PySide6.QtWidgets import QApplication
from button_holder import ButtonHolder
import sys

app = QApplication(sys.argv)


window = ButtonHolder()
window.show()
app.exec()
"""

""" Example 2: PySide6 Application with a Clickable Button
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider
import sys


def button_clicked(data):
    print("Button clicked! Status:", data)


app = QApplication(sys.argv)

button = QPushButton("Click me!")
button.setCheckable(True)
button.clicked.connect(button_clicked)

button.show()
app.exec()
"""
""" Example 3: PySide6 Application with a Slider
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSlider
import sys


def respond_to_slider(data):
    print("Slider moved to", data)


app = QApplication(sys.argv)
slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(25)

slider.valueChanged.connect(respond_to_slider)
slider.show()

app.exec()
"""
from PySide6.QtWidgets import QApplication
from my_library import rockWidget
import sys

app = QApplication(sys.argv)
window = rockWidget()
window.show()

app.exec()
