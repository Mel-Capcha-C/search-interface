from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QSizePolicy,
    QStatusBar,
    QWidget,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QRadioButton,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon, QPixmap


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
        button_widget = QWidget()

        button_hard = QPushButton("Hard")
        button_hard.clicked.connect(self.button_clicked_hard)

        button_critical = QPushButton("Critical")
        button_critical.clicked.connect(self.button_clicked_critical)

        button_question = QPushButton("Question")
        button_question.clicked.connect(self.button_clicked_question)

        button_about = QPushButton("About")
        button_about.clicked.connect(self.button_clicked_about)

        button_layout.addWidget(button_hard)
        button_layout.addWidget(button_critical)
        button_layout.addWidget(button_question)
        button_layout.addWidget(button_about)

        button_widget.setLayout(button_layout)

        # Label and line edit
        label = QLabel("Enter your name:")
        self.line_edit = QLineEdit()
        self.line_edit.cursorPositionChanged.connect(self.cursor_position_changed)
        self.line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Line edit button and label to hold text

        name_button = QPushButton("Submit")
        name_button.clicked.connect(self.submit_name)
        self.text_holder_label = QLabel("I am here")

        # Label and line edit layout
        label_layout = QHBoxLayout()
        label_layout.addWidget(label, 1)
        label_layout.addWidget(self.line_edit, 2)

        le_layout = QVBoxLayout()
        le_layout.addLayout(label_layout)
        le_layout.addWidget(name_button)
        le_layout.addWidget(self.text_holder_label)

        # Text edit
        self.text_edit = QTextEdit()

        # Text edit buttons
        te_current_text_button = QPushButton("Current Text")
        te_current_text_button.clicked.connect(self.te_current_text_button_clicked)

        te_copy_button = QPushButton("Copy")
        # Connect directly to QTextEdit's copy slot
        te_copy_button.clicked.connect(self.text_edit.copy)

        te_cut_button = QPushButton("Cut")
        te_cut_button.clicked.connect(self.text_edit.cut)

        te_paste_button = QPushButton("Paste")
        te_paste_button.clicked.connect(self.text_edit.paste)

        te_undo_button = QPushButton("Undo")
        te_undo_button.clicked.connect(self.text_edit.undo)

        te_redo_button = QPushButton("Redo")
        te_redo_button.clicked.connect(self.text_edit.redo)

        te_set_plain_text_button = QPushButton("Set Plain Text")
        te_set_plain_text_button.clicked.connect(self.set_plain_text)

        te_set_html_button = QPushButton("Set HTML")
        te_set_html_button.clicked.connect(self.set_html)

        te_clear_button = QPushButton("Clear Text")
        te_clear_button.clicked.connect(self.text_edit.clear)

        # Text edit layout
        te_button_layout = QGridLayout()

        te_button_layout.addWidget(te_copy_button, 0, 0)
        te_button_layout.addWidget(te_paste_button, 0, 1)
        te_button_layout.addWidget(te_cut_button, 0, 2)
        te_button_layout.addWidget(te_undo_button, 0, 3)
        te_button_layout.addWidget(te_redo_button, 0, 4)
        te_button_layout.addWidget(
            te_set_plain_text_button, 1, 0, 1, 3
        )  # Take up 1 row and 3 columns
        te_button_layout.addWidget(
            te_current_text_button, 2, 0, 1, 3
        )  # Take up 1 row and 3 columns
        te_button_layout.addWidget(
            te_set_html_button, 1, 3, 1, 2
        )  # Take up 1 row and 2 columns
        te_button_layout.addWidget(
            te_clear_button, 2, 3, 1, 2
        )  # Take up 1 row and 2 columns

        te_layout = QVBoxLayout()
        te_layout.addLayout(te_button_layout)
        te_layout.addWidget(self.text_edit)

        # Image label
        image_label = QLabel()
        image_label.setPixmap(QPixmap("Images/Panda_logo.jpg").scaledToHeight(300))

        # Check boxes
        os = QGroupBox("Choose operating system")
        windows = QCheckBox("Windows")
        windows.toggled.connect(lambda checked: print(f"Windows toggled: {checked}"))
        windows.setChecked(True)  # Set Windows checkbox to be checked by default
        linux = QCheckBox("Linux")
        linux.toggled.connect(lambda checked: print(f"Linux toggled: {checked}"))
        mac = QCheckBox("Mac")
        mac.toggled.connect(lambda checked: print(f"Mac toggled: {checked}"))

        os_layout = QVBoxLayout()
        os_layout.addWidget(windows)
        os_layout.addWidget(linux)
        os_layout.addWidget(mac)
        os.setLayout(os_layout)
        os.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        os.exclusive = False
        # Radio buttons
        answer_group = QGroupBox("Choose an answer")
        answer_a = QRadioButton("Answer a")
        answer_b = QRadioButton("Answer b")
        answer_c = QRadioButton("Answer c")

        answer_group.exclusive = True  # Only one radio button can be selected at a time

        answer_layout = QVBoxLayout()
        answer_layout.addWidget(answer_a)
        answer_layout.addWidget(answer_b)
        answer_layout.addWidget(answer_c)

        answer_group.setLayout(answer_layout)

        # Primary Layout

        primary_layout = QVBoxLayout()
        primary_layout.addLayout(le_layout)
        primary_layout.addSpacing(20)
        primary_layout.addLayout(te_layout)
        primary_layout.addSpacing(20)
        primary_layout.addWidget(button_widget)
        primary_layout.addSpacing(20)
        primary_layout.addWidget(image_label)

        primary_widget = QWidget()
        primary_widget.setLayout(primary_layout)
        primary_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Secondary layout for checkboxes and radio buttons
        secondary_layout = QVBoxLayout()
        secondary_layout.addWidget(os)
        secondary_layout.addSpacing(20)
        secondary_layout.addWidget(answer_group)

        main_layout = QHBoxLayout()
        main_layout.addWidget(primary_widget)
        main_layout.addSpacing(20)
        main_layout.addLayout(secondary_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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

    def button_clicked_question(self):
        ret = QMessageBox.question(
            self,
            "Message Title",
            "Question message",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes,
        )

        if ret == QMessageBox.Yes:
            print("User clicked Yes!")
        elif ret == QMessageBox.No:
            print("User clicked No!")
        else:
            print("User clicked Cancel!")

    def button_clicked_about(self):
        QMessageBox.about(
            self,
            "Message Title",
            "About message: This is a PySide6 application demonstrating various QMessageBox types.",
        )

    def submit_name(self):
        name = self.line_edit.text()
        self.text_holder_label.setText(f"Hello, {name}!")
        print(f"User submitted name: {name}")

    def cursor_position_changed(self, old, new):
        print(f"Cursor position changed from {old} to {new}")

    def set_plain_text(self):
        self.text_edit.setPlainText("My name is Rock")

    def set_html(self):
        self.text_edit.setHtml(
            "<h1 style='color: red;'>My name is Rock</h1><p>This is a paragraph.</p>"
        )

    def te_current_text_button_clicked(self):
        current_text = self.text_edit.toPlainText()
        print("Current text in QTextEdit:", current_text)
