from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTableWidget,  QHeaderView,  QLineEdit, QFormLayout,
    QDesktopWidget, QStackedWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure

def initialise(self):
        # Window title and icon setup
        self.setWindowTitle('MindAble Time Series Segmentation Tool')
        self.setWindowIcon(QIcon('assets\mindable_icon.PNG'))

        # Get the screen size and set the window size to 1/2 of the screen dimensions
        screen_geometry = QDesktopWidget().screenGeometry()
        window_width, window_height = screen_geometry.width() // 2, screen_geometry.height() // 1.4

        self.setGeometry(
            (screen_geometry.width() - window_width) // 2,  # Center horizontally
            (screen_geometry.height() - window_height) // 2,  # Center vertically
            window_width, window_height  # Set window size
        )

        # List to store the file paths to prevent duplicates
        self.selected_files = []
        self.mne_data_objects = {}  # Dictionary to store MNE data objects
        self.intervals_per_recording = 2  # Store num intervals value

        # Create stacked widget for navigation
        self.stacked_widget = QStackedWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        # Session Selection Page
        self.session_page = QWidget(self)
        self.session_page_layout = QVBoxLayout(self.session_page)

        self.import_button = QPushButton("Import Data", self)
        self.import_button.clicked.connect(self.open_file_dialog)
        self.session_page_layout.addWidget(self.import_button)

        self.table = QTableWidget(self)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Sessions"])
        header_item = self.table.horizontalHeaderItem(0)
        if header_item:
            header_item.setFlags(header_item.flags() & ~Qt.ItemIsEditable)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.selectionModel().selectionChanged.connect(self.update_remove_button_state)
        self.session_page_layout.addWidget(self.table)

        self.remove_button = QPushButton("Remove Selected", self)
        self.remove_button.clicked.connect(self.remove_selected_files)
        self.remove_button.setEnabled(False)
        self.session_page_layout.addWidget(self.remove_button)

        form_layout = QFormLayout()
        self.intervals_input = QLineEdit(self)
        self.intervals_input.setPlaceholderText("Enter an integer > 0")
        self.intervals_input.textChanged.connect(self.update_next_button_state)
        form_layout.addRow("Intervals Per Recording:", self.intervals_input)
        self.session_page_layout.addLayout(form_layout)

        # Add input field for project directory name
        form_layout = QFormLayout()  # Create a form layout
        self.project_dir_input = QLineEdit(self)
        self.project_dir_input.setPlaceholderText("new_directory_name")
        form_layout.addRow("Enter Project Directory Name:", self.project_dir_input)  # Add the label and input field pair
        self.project_dir_input.textChanged.connect(self.update_next_button_state)

        # Add the form layout to the session page layout
        self.session_page_layout.addLayout(form_layout)

        h_layout = QHBoxLayout()
        self.next_button = QPushButton("Next", self)
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.change_layout)
        h_layout.addWidget(self.next_button)
        self.session_page_layout.addLayout(h_layout)

        self.stacked_widget.addWidget(self.session_page)

        # Session Details Page
        self.details_page = QWidget(self)
        self.details_page_layout = QVBoxLayout(self.details_page)

        # Embedded plot area with dynamic size
        scaling_factor = 140 # Pixel-inches scaling factor
        self.canvas = FigureCanvas(Figure(figsize=(8, window_height // scaling_factor)))
        self.ax = self.canvas.figure.add_subplot(111)

        # Add Matplotlib toolbar for interactivity
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.details_page_layout.addWidget(self.toolbar)

        self.details_page_layout.addWidget(self.canvas)  # Add the canvas after the toolbar

        # Add a table for sessions instead of the list
        self.session_table = QTableWidget(self)
        self.session_table.setColumnCount(2 * self.intervals_per_recording + 1)
        self.session_table.setHorizontalHeaderLabels(["Sessions"])
        self.session_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # self.session_table.itemClicked.connect(self.plot_eeg_channels)  # Connect selection change to the plot function
        self.session_table.itemClicked.connect(self.set_save_off)  # Connect selection change to the plot function
        self.details_page_layout.addWidget(self.session_table)

        # Fix the layout to stretch and remove unwanted white space
        h_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply", self)
        self.back_button = QPushButton("Back", self)
        self.save_button = QPushButton("Save", self)
        h_layout.addWidget(self.back_button)
        h_layout.addWidget(self.apply_button)  # Add the Apply button to the same layout as Back and Save
        h_layout.addWidget(self.save_button)
        
        self.details_page_layout.addLayout(h_layout)

        self.details_page_layout.addStretch(1)  # Add a stretch factor to ensure the layout fills the available space

        self.stacked_widget.addWidget(self.details_page)

        self.back_button.clicked.connect(self.go_back)

        self.apply_button.clicked.connect(self.highlight_invalid_times)

        self.setup_item_changed_signals()
        
        self.setup_item_clicked_signals()

        self.save_button.clicked.connect(self.save_cropped_data_as_edf)

        self.session_table.itemClicked.connect(self.clear_highlight)

        self.session_table.currentCellChanged.connect(self.row_selection_changed)