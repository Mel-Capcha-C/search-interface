from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QGridLayout,
    QGroupBox,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
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
    QListWidget,
    QComboBox,
    QTableView,
    QHeaderView,
)
from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QSize,
    QModelIndex,
    QSortFilterProxyModel,
)
from PySide6.QtGui import QAction, QIcon, QPixmap, QColor, QFont, QPalette
import pandas as pd
import sys

# sys.path.insert(0, "C:\\Users\\PC\\Data\\Documents\\git\\search-interface\\config")
sys.path.insert(
    0, "C:\\Users\\Mel_C\\Data\\Documents\\git\\Mel-Capcha-C\\search-interface\\config"
)
from product_config import config

ALL = "(Todos)"

# QAbstractTableModel constants
# BG_ODD = "#F1B8B8"  # BackgroundRole color for odd rows
# BG_EVEN = "#F1F5F9"  # BackgroundRole color for even rows
# BG_HEADER = "#FF5858"  # Light blue bg

BG_ODD = "#43484A"  # BackgroundRole color for odd rows
BG_EVEN = "#363839"  # BackgroundRole color for even rows
BG_HEADER = "#570B3F"  # Light blue bg

# Human-friendly header names for the table
HEADER_LABELS = {
    "Código": "Código",
    "Código Sistema": "Cód. Sistema",
    "Conexión": "Conexión",
    "Tipo Velocidad": "Tipo Velocidad",
    "Potencia": "Potencia (W)",
    "Ratio": "Ratio",
    "Stock Total": "Stock",
    "Descripción\nNueva": "Descripción",
}


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


class DataFrameModel(QAbstractTableModel):
    """Read-only Qt model backed by a pandas DataFrame."""

    def __init__(self, df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._df = df.reset_index(drop=True)

    def update(self, df: pd.DataFrame):
        self.beginResetModel()
        self._df = df.reset_index(drop=True)
        self.endResetModel()

    # ── required overrides ──────────────────────────────────────────────────
    def rowCount(self, parent=QModelIndex()):
        return len(self._df)

    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        value = self._df.iloc[index.row(), index.column()]

        if role == Qt.DisplayRole:
            if pd.isna(value):
                return "—"
            # Format Ratio as "X:1"
            col = self._df.columns[index.column()]
            if col == "Ratio":
                return f"{int(value)}:1"
            if col == "Potencia":
                return f"{int(value)} W"
            return str(value)

        if role == Qt.TextAlignmentRole:
            col = self._df.columns[index.column()]
            if col in ("Potencia", "Ratio", "Stock Total"):
                return int(Qt.AlignCenter)
            return int(Qt.AlignVCenter | Qt.AlignLeft)

        if role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QColor(BG_EVEN)
            return QColor(BG_ODD)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col = self._df.columns[section]
                return HEADER_LABELS.get(col, col)
            return str(section + 1)

        if role == Qt.FontRole and orientation == Qt.Horizontal:
            f = QFont()
            f.setBold(True)
            return f

        if role == Qt.BackgroundRole and orientation == Qt.Horizontal:
            return QColor(BG_HEADER)

        return None

    # https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.QAbstractItemModel.dataChanged
    """Methods that make the table editable
    def setData(self, index, value, /, role=...):
        if role == Qt.EditRole:
            self._df.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    """


class RGMainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("RG Interface")
        self.app = app  # Declare an app member
        self._load_data()
        self._build_ui()

    def _load_data(self):
        # excel_file_path = "C:/Users/PC/Data/Documents/Chamba/WESMOTOR/Reportes/Stock/Microrreductores.xlsx"
        excel_file_path = "C:/Users/Mel_C/Data/Documents/Chamba/WESMOTOR/Reportes/Microrreductores.xlsx"
        self.df = pd.read_excel(excel_file_path, sheet_name="Microrreductores")
        # self.df.to_csv("Microrreductores")

        self.features = config["Microrreductor"]["features"]
        print(self.features)

        for feature in self.features:
            if feature not in self.df.columns:
                raise ValueError(
                    f"Column '{feature}' not found in Excel. Check config features or Excel columns!"
                )

    def _build_ui(self):
        # Menubar and menus
        self.ly_main = QVBoxLayout()
        self.wg_central = QWidget()
        self.wg_central.setLayout(self.ly_main)
        self.setCentralWidget(self.wg_central)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")

        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)

        lb_title = QLabel("Búsqueda Productos")
        lb_title.setStyleSheet("font-size: 20px; font-weight: bold")
        lb_logo = QLabel()
        lb_logo.setPixmap(QPixmap("Images/logo_R_G_gray.jpg").scaledToHeight(50))
        lb_logo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        ly_title = QHBoxLayout()
        wg_title = QWidget()
        wg_title.setLayout(ly_title)
        ly_title.addWidget(lb_title, 2)
        ly_title.addWidget(lb_logo, 1)
        # Nomenclature:
        # lb => Label
        # cb => ComboBox
        # wg => Widget
        # ly => Layout
        # pb => PushButton

        # Label and combo box for products
        lb_select_product = QLabel("Seleccione Producto:")
        lb_select_product.setStyleSheet(
            "background-color: #E03232; color: white; padding: 5px;"
        )
        lb_select_product.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        cb_select_product = QComboBox(self)
        cb_select_product.addItems(config.keys())
        cb_select_product.setCurrentIndex(1)
        cb_select_product.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # cb_productos.setStyleSheet("QComboBox::drop-down { background-color: red; }")
        cb_select_product.currentTextChanged.connect(self.current_product_changed)

        wg_select_product = QWidget()
        wg_select_product.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        ly_select_product = QHBoxLayout()
        ly_select_product.addWidget(lb_select_product)
        ly_select_product.addWidget(cb_select_product)
        wg_select_product.setLayout(ly_select_product)

        # ComboBox Features (Filter Panel)
        self.wg_select_features = QWidget()
        self.ly_select_features = QVBoxLayout()
        self.wg_select_features.setLayout(self.ly_select_features)
        self.wg_select_features.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.cb_select_features = {}

        # ── Results table ──────────────────────────────────────────────────
        self.model = DataFrameModel(self.df[self.features])
        self.table = QTableView()
        self.table.setModel(self.model)
        # https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QHeaderView.html#PySide6.QtWidgets.QHeaderView.ResizeMode
        # QHeaderView.ResizeMode.Interactive
        # QHeaderView.ResizeMode.Fixed
        # QHeaderView.ResizeMode.Stretch
        # QHeaderView.ResizeMode.ResizeToContents
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QHeaderView::section:checked {
                background-color: "#8A2A71";
            }
            """)

        # This property holds whether the sections containing selected items are highlighted. By default, this property is false.
        self.table.horizontalHeader().setHighlightSections(True)
        # https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QAbstractItemView.html#PySide6.QtWidgets.QAbstractItemView.SelectionBehavior
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        # https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QAbstractItemView.html#PySide6.QtWidgets.QAbstractItemView.EditTrigger
        # property editTriggers: This property holds which actions will initiate item editing.

        # self.table.setEditTriggers(QTableView.EditTrigger.DoubleClicked)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        self.table.setAlternatingRowColors(False)  # Handled in QAbstractTableModel
        self.table.setSortingEnabled(True)
        self.table.setShowGrid(False)

        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setVisible(True)

        # Create Code Button
        pb_create_code = QPushButton("Create code")
        pb_create_code.clicked.connect(self.create_code)

        # Layout
        self.ly_main.addWidget(wg_title)
        self.ly_main.addWidget(wg_select_product)
        self.ly_main.addWidget(self.wg_select_features)
        self.ly_main.addWidget(self.table)
        self.ly_main.addWidget(pb_create_code)
        # Tab Widget
        # self.tab_widget = QTabWidget()
        # self.tab_widget.addTab(central_widget, "Code Generator")
        # self.setCentralWidget(self.tab_widget)

    # ── Population helpers ────────────────────────────────────────────────
    def _populate_conexion(self):
        self.cb_select_features["Conexión"].blockSignals(True)
        self.cb_select_features["Conexión"].clear()
        self.cb_select_features["Conexión"].addItem(ALL)
        for val in sorted(self.df["Conexión"].dropna().unique()):
            self.cb_select_features["Conexión"].addItem(str(val))
        self.cb_select_features["Conexión"].blockSignals(False)

    def _populate_combo(self, combo: QComboBox, series: pd.Series, fmt=str):
        """Refill a combo while preserving the current selection if possible."""
        current = combo.currentText()
        combo.blockSignals(True)
        combo.clear()
        combo.addItem(ALL)
        for val in sorted(series.dropna().unique()):
            combo.addItem(fmt(val))
        idx = combo.findText(current)
        combo.setCurrentIndex(idx if idx >= 0 else 0)
        combo.blockSignals(False)

    def _fmt_ratio(self, val):
        try:
            return f"{int(float(val))}:1"
        except Exception:
            return str(val)

    def _fmt_potencia(self, val):
        try:
            return f"{int(float(val))} W"
        except Exception:
            return str(val)

    def _on_conexion_changed(self):
        conexion = self.cb_select_features["Conexión"].currentText()
        is_mono = conexion == "Monofásico"

        # Show/hide Tipo Velocidad depending on Conexión
        self.cb_select_features["Tipo Velocidad"].setVisible(is_mono or conexion == ALL)

        if not (is_mono or conexion == ALL):
            self.cb_select_features["Tipo Velocidad"].blockSignals(True)
            self.cb_select_features["Tipo Velocidad"].setCurrentIndex(0)
            self.cb_select_features["Tipo Velocidad"].blockSignals(False)

        self._apply_filters()

    def _apply_filters(self):
        df = self.df.copy()

        # 1. Conexión
        conexion = self.cb_select_features["Conexión"].currentText()
        if conexion != ALL:
            df = df[df["Conexión"] == conexion]
  
        self._populate_combo(
            self.cb_select_features["Tipo Velocidad"],
            df["Tipo Velocidad"]
            if conexion in (ALL, "Monofásico")
            else pd.Series(dtype=str),
        )

        # 2. Tipo Velocidad (only for Monofásico or ALL)
        tipo_vel = self.cb_select_features["Tipo Velocidad"].currentText()

        if tipo_vel != ALL and self.cb_select_features["Tipo Velocidad"].isVisible():
            df = df[df["Tipo Velocidad"] == tipo_vel]

        #Re-populate downstream combos based on current filtered pool
        self._populate_combo(
            self.cb_select_features["Potencia"],
            df["Potencia"],
            self._fmt_potencia,
        )

        self._populate_combo(
            self.cb_select_features["Ratio"], df["Ratio"], self._fmt_ratio
        )

        # 3. Potencia
        potencia_txt = self.cb_select_features["Potencia"].currentText()
        if potencia_txt != ALL:
            try:
                potencia_val = int(potencia_txt.replace(" W", "").strip())
                df = df[df["Potencia"] == potencia_val]
            except ValueError:
                pass

        # # 4. Ratio
        ratio_txt = self.cb_select_features["Ratio"].currentText()
        if ratio_txt != ALL:
            try:
                ratio_val = float(ratio_txt.replace(":1", "").strip())
                df = df[df["Ratio"] == ratio_val]
            except ValueError:
                pass

        # Debug
        print("Ah")
        print(df)
        # Update table
        self.model.update(df[self.features])
        # total = len(self.df_full)
        # shown = len(df)
        # self.status.showMessage(
        #     f"Mostrando {shown} de {total} productos   •   "
        #     f"{'Todos los filtros activos' if shown < total else 'Sin filtros aplicados'}"
        # )

    def _reset_filters(self):
        for combo in (
            self.cb_conexion,
            self.cb_tipo_vel,
            self.cb_potencia,
            self.cb_ratio,
        ):
            combo.blockSignals(True)
            combo.setCurrentIndex(0)
            combo.blockSignals(False)
        self.cb_tipo_vel_widget.setVisible(True)
        self._apply_filters()

    def quit(self):
        self.app.quit()

    def create_code(self):
        print("Creating code for selected product...")

    def current_product_changed(self, text):
        product = text
        config_producto = config[product]

        print("Creating Combo Boxes")
        # Crear nuevos campos

        # Clear previous layout

        for ii in reversed(range(self.ly_select_features.count())):
            # If this item manages a QWidget , returns that widget. Otherwise, None is returned.
            wg_single_feature = self.ly_select_features.itemAt(ii).widget()
            if wg_single_feature:
                wg_single_feature.deleteLater()

        self.cb_select_features.clear()

        for features in config_producto["features"]:
            wg_single_feature = QWidget()
            ly_single_feature = QHBoxLayout()
            wg_single_feature.setLayout(ly_single_feature)

            lb_single_feature = QLabel(features)

            cb_single_feature = QComboBox()

            ly_single_feature.addWidget(lb_single_feature)
            ly_single_feature.addWidget(cb_single_feature)

            self.ly_select_features.addWidget(wg_single_feature)
            self.cb_select_features[features] = cb_single_feature
            # self.central_widget.setLayout(self.main_layout)

        # Inicializar campos
        self.cb_select_features["Conexión"].currentIndexChanged.connect(
            self._on_conexion_changed
        )
        self.cb_select_features["Tipo Velocidad"].currentIndexChanged.connect(
            self._apply_filters
        )
        self.cb_select_features["Potencia"].currentIndexChanged.connect(
            self._apply_filters
        )
        self.cb_select_features["Ratio"].currentIndexChanged.connect(
            self._apply_filters
        )
        self._populate_conexion()

    def initialize_features(self, product):
        data = config[product]["data"]  # raíz
        features = config[product]["features"]

        for campo in data.keys():
            print(f"Campo, {campo}")

            # valor = self.combos[campo].currentText()

            # if not valor:
            #     break

            # if valor in data:
            #     data = data[valor]
            # else:
            #     break

        for feature in features:
            print(f"{feature}: ", self.cb_select_features[feature])
        # return data


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

        # Radio buttons
        answer_group = QGroupBox("Choose an answer")
        answer_a = QRadioButton("Answer a")
        answer_b = QRadioButton("Answer b")
        answer_c = QRadioButton("Answer c")

        exclusive_button_group = (
            QButtonGroup()
        )  # Only one radio button can be selected at a time
        exclusive_button_group.addButton(answer_a)
        exclusive_button_group.addButton(answer_b)
        exclusive_button_group.addButton(answer_c)

        answer_layout = QVBoxLayout()
        answer_layout.addWidget(answer_a)
        answer_layout.addWidget(answer_b)
        answer_layout.addWidget(answer_c)

        answer_group.setLayout(answer_layout)

        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        self.list_widget.addItem("Uno")
        self.list_widget.addItems(["Dos", "Tres"])

        self.list_widget.currentItemChanged.connect(self.lw_current_item_changed)
        self.list_widget.currentTextChanged.connect(self.lw_current_text_changed)

        lw_button_add_item = QPushButton("Add Item")
        lw_button_add_item.clicked.connect(self.lw_add_item)

        lw_button_delete_item = QPushButton("Delete Item")
        lw_button_delete_item.clicked.connect(self.lw_delete_item)

        lw_button_item_count = QPushButton("Item Count")
        lw_button_item_count.clicked.connect(self.lw_item_count)

        lw_button_selected_items = QPushButton("Selected Items")
        lw_button_selected_items.clicked.connect(self.lw_selected_items)

        lw_button_layout = QVBoxLayout()
        lw_button_layout.addWidget(lw_button_add_item)
        lw_button_layout.addWidget(lw_button_delete_item)
        lw_button_layout.addWidget(lw_button_item_count)
        lw_button_layout.addWidget(lw_button_selected_items)

        lw_layout = QHBoxLayout()
        lw_layout.addWidget(self.list_widget, 2)
        lw_layout.addLayout(lw_button_layout, 1)

        lw_widget = QWidget()
        lw_widget.setLayout(lw_layout)

        # Tab Widget
        tab_widget = QTabWidget()
        first_tab = QWidget()
        second_tab = QWidget()

        tw_label = QLabel("This is the second tab")
        tw_button1 = QPushButton("Button 1")
        tw_button1.setCheckable(True)
        tw_button1.clicked.connect(
            lambda checked: print(f"Button 1 in second tab clicked: {checked}")
        )

        # Combo Box
        self.combo_box = QComboBox(self)
        cb_label = QLabel("Choose a planet:")
        # Add planets
        self.combo_box.addItems(["Earth", "Venus", "Mars", "Pluton", "Jupiter"])

        cb_button_widget = QWidget()

        cb_button_current_value = QPushButton("Current value")
        cb_button_current_value.clicked.connect(self.cb_current_value)

        cb_button_set_current = QPushButton("Set value")
        cb_button_set_current.clicked.connect(self.cb_set_current)

        cb_button_get_values = QPushButton("Get values")
        cb_button_get_values.clicked.connect(self.cb_get_values)

        cb_button_layout = QHBoxLayout()
        cb_button_layout.addWidget(cb_button_current_value)
        cb_button_layout.addWidget(cb_button_set_current)
        cb_button_layout.addWidget(cb_button_get_values)

        cb_button_widget.setLayout(cb_button_layout)

        # Second tab layout
        tw_second_layout = QVBoxLayout()
        tw_second_layout.addWidget(tw_label)
        tw_second_layout.addWidget(tw_button1)
        tw_second_layout.addSpacing(20)
        tw_second_layout.addWidget(cb_label)
        tw_second_layout.addWidget(self.combo_box)
        tw_second_layout.addWidget(cb_button_widget)

        second_tab.setLayout(tw_second_layout)

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
        secondary_layout.addSpacing(20)
        secondary_layout.addWidget(lw_widget)

        first_tab.setLayout(secondary_layout)
        tab_widget.addTab(first_tab, "First Tab")
        tab_widget.addTab(second_tab, "Second Tab")

        main_layout = QHBoxLayout()
        main_layout.addWidget(primary_widget)
        main_layout.addSpacing(20)
        main_layout.addWidget(tab_widget)

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

    def lw_current_item_changed(self, item):
        print("Current item:", item.text())

    def lw_current_text_changed(self, text):
        print("Current text changed:", text)

    def lw_add_item(self):
        new_item_text = f"Item {self.list_widget.count() + 1}"
        self.list_widget.addItem(new_item_text)

    def lw_delete_item(self):
        # self.list_widget.takeItem(self.list_widget.currentRow())
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            print(f"Deleting item: {item.text()}")
            self.list_widget.takeItem(self.list_widget.row(item))

    def lw_item_count(self):
        count = self.list_widget.count()
        print(f"Item count: {count}")

    def lw_selected_items(self):
        selected_items = self.list_widget.selectedItems()
        selected_texts = [item.text() for item in selected_items]
        print("Selected items:", selected_texts)

    def cb_current_value(self):
        current_value = self.combo_box.currentText()
        print(
            "Current combo box value:",
            current_value,
            "Index:",
            self.combo_box.currentIndex(),
        )

    def cb_set_current(self):
        self.combo_box.setCurrentIndex(2)  # Set to "Mars"

    def cb_get_values(self):
        count = self.combo_box.count()
        values = [self.combo_box.itemText(i) for i in range(count)]
        print("Combo box values:", values)
