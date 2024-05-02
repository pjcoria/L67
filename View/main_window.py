# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:39:56 2024

@author: Laboratorio
"""
import os
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
import pyqtgraph as pg

#%%

class MainWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        self.setWindowTitle('Scan Window')
        self.experiment=experiment
        
        self.central_widget = QWidget()
        self.button_widgets = QWidget()
        self.start_button = QPushButton('Start', self.button_widgets)
        self.stop_button = QPushButton('Stop', self.button_widgets)
        self.plot_widget = pg.PlotWidget(title='Plotting t vs V')
        self.plot =self.plot_widget.plot([0], [0])
        
        layout = QHBoxLayout(self.button_widgets)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        
        central_layout = QVBoxLayout(self.central_widget)
        central_layout.addWidget(self.button_widgets)
        central_layout.addWidget(self.plot_widget)
        
        self.setCentralWidget(self.central_widget)
        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        
        
    def start_scan(self):
        self.timer.start(50)
        print('Scan Started')
        
    def stop_scan(self):
        self.timer.stop()
        print('Scan Stopped')
        
    def update_plot(self):
        self.experiment.start_scan()
        self.plot.setData(self.experiment.scan_data[0],self.experiment.scan_data[1])