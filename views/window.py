from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout,
    QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget
)
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.data_model import Data
from controllers.data_loader import load_data_file
from controllers.plot_controller import plot_graphs

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MatStat')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(1200, 600) 

        self.data_model = Data()
        self.data = None

        # widgets
        self.load_data_button = QPushButton('Load Data')
        self.load_data_button.setFixedSize(80, 30)
        self.load_data_button.clicked.connect(lambda: load_data_file(self))

        # bins
        self.bins_label = QLabel('Number of Classes:')
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 100)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setEnabled(False)

        # plot 
        self.plot_button = QPushButton('Plot Graphs')
        self.plot_button.setEnabled(False)
        self.plot_button.clicked.connect(lambda: plot_graphs(self))

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Histogram tab
        self.hist_figure = Figure(figsize=(8, 6))
        self.hist_canvas = FigureCanvas(self.hist_figure)
        self.hist_ax = self.hist_figure.add_subplot(111)
        
        # EDF tab
        self.edf_figure = Figure(figsize=(8, 6))
        self.edf_canvas = FigureCanvas(self.edf_figure)
        self.edf_ax = self.edf_figure.add_subplot(111)
        
        # Add tabs
        self.tab_widget.addTab(self.hist_canvas, "Histogram")
        self.tab_widget.addTab(self.edf_canvas, "Empirical Distribution Function")

        # tables
        self.char_table = QTableWidget()
        self.char_table.setColumnCount(2)
        self.char_table.setHorizontalHeaderLabels(['Characteristic', 'Value'])
        self.char_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.char_table.setMinimumWidth(250)  

        self.ci_table = QTableWidget()
        self.ci_table.setColumnCount(3)  
        self.ci_table.setHorizontalHeaderLabels(['Characteristic', 'Lower conf_interval', 'Upper conf_interval'])
        self.ci_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ci_table.setMinimumWidth(250)

        # layout
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.load_data_button)
        controls_layout.addWidget(self.bins_label)
        controls_layout.addWidget(self.bins_spinbox)
        controls_layout.addWidget(self.plot_button)
        controls_layout.addStretch()

        # Create a vertical layout for tables
        tables_layout = QVBoxLayout()
        tables_layout.addWidget(self.char_table)
        tables_layout.addWidget(self.ci_table)

        # Main layout with plot and tables side by side
        plot_and_tables_layout = QHBoxLayout()
        plot_and_tables_layout.addWidget(self.tab_widget, stretch=2)
        plot_and_tables_layout.addLayout(tables_layout, stretch=1)

        # Final vertical layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(plot_and_tables_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)