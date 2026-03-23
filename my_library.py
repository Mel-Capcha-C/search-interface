from PySide6.QtWidgets import (
    QStatusBar,
    QWidget,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon


class rockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RockWidget")
        button1 = QPushButton("Click me 1!")
        button1.clicked.connect(self.button1_clicked)
        button2 = QPushButton("Click me 2!")
        button2.clicked.connect(self.button2_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        self.setLayout(button_layout)

    def button1_clicked(self):
        print("Button 1 clicked!")

    def button2_clicked(self):
        print("Button 2 clicked!")


class rockMainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Custom MainWindow")
        self.app = app  # Declare an app member

        # Menubar and menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Cut")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        # Toolbar
        toolbar = self.addToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))

        toolbar.addAction(quit_action)

        action1 = QAction("Some Action", self)
        action1.setStatusTip("Status message for some action")
        action1.triggered.connect(self.toolbar_button_click)
        action1.setCheckable(True)
        toolbar.addAction(action1)

        action2 = QAction(QIcon("Images\\music.jpg"), "Some other action", self)
        action2.setStatusTip("Status message for some other action")
        action2.triggered.connect(self.toolbar_button_click)
        toolbar.addAction(action2)

        toolbar.addSeparator()
        toolbar.addWidget(QPushButton("Click here"))

        # Statusbar
        self.setStatusBar(QStatusBar(self))

        button_layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        button_hard = QPushButton("Hard")
        button_hard.clicked.connect(self.button_clicked_hard)

        button_critical = QPushButton("Critical")
        button_critical.clicked.connect(self.button_clicked_critical)

        button_layout.addWidget(button_hard)
        button_layout.addWidget(button_critical)

        central_widget.setLayout(button_layout)

    def toolbar_button_click(self):
        self.statusBar().showMessage("Toolbar button clicked!", 3000)

    def quit(self):
        self.app.quit()

    def button_clicked_hard(self):
        message = QMessageBox()
        message.setMinimumSize(700, 200)
        message.setWindowTitle("Message Title")
        message.setText("Something happened!")
        message.setInformativeText("Do you want to do something about it?")
        message.setIcon(QMessageBox.Icon.Critical)
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # QMessageBox.Ok is an alias for QMessageBox.StandardButton.Ok)
        message.setDefaultButton(QMessageBox.StandardButton.Ok)
        ret = message.exec()

        if ret == QMessageBox.Ok:
            print("User clicked OK!")
        else:
            print("User clicked Cancel!")

    def button_clicked_critical(self):
        ret = QMessageBox.critical(
            self,
            "Message Title",
            "Critical message",
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Ok,
        )

        if ret == QMessageBox.Ok:
            print("User clicked OK!")
        else:
            print("User clicked Cancel!")
