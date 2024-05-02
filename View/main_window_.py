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
import numpy as np

#%%

class MainWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(base_dir, 'GUI', 'main_window.ui')
        uic.loadUi(ui_file, self)
        
        self.experiment=experiment
        
        self.plot_widget = pg.PlotWidget(title='Plotting t vs V')
        self.plot =self.plot_widget.plot([0], [0])
        
        layout=self.central_widget.layout()
        layout.addWidget(self.plot_widget)
        
        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)
        self.update_button.clicked.connect(self.update_parameters)
        self.save_button.clicked.connect(self.save_screen)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        
        self.comboBox.addItem('CH2_PE')
        self.comboBox.addItem('CH2_NE')
        self.comboBox.addItem('CH1_PE')
        self.comboBox.addItem('CH1_NE')
        
        self.DF_spinBox.setValue(int(np.log2(self.experiment.config['Scan']['DF'])))
        self.delay_lineEdit.setText(str(self.experiment.config['Scan']['T_delay']))
        self.comboBox.setCurrentText(self.experiment.config['Scan']['T_source'])
        self.N_lineEdit.setText(str(self.experiment.config['Scan']['N_sample']))
        self.T_level_lineEdit.setText(str(self.experiment.config['Scan']['T_level']))
        
    def start_scan(self):
        self.timer.start(50)
        print('Scan Started')
        
    def stop_scan(self):
        self.timer.stop()
        print('Scan Stopped')
        
    def update_plot(self):
        self.experiment.start_scan()
        self.plot.setData(self.experiment.scan_data[0],self.experiment.scan_data[1])
        
    def update_parameters(self):
        self.experiment.config['Scan']['DF']=int(2**(self.DF_spinBox.value()))
        self.experiment.config['Scan']['T_delay']=int(self.delay_lineEdit.text())
        self.experiment.config['Scan']['T_source']=self.comboBox.currentText()
        self.experiment.config['Scan']['N_sample']=int(self.N_lineEdit.text())
        self.experiment.config['Scan']['T_level']=float(self.T_level_lineEdit.text())
        
    def save_screen(self):
        self.experiment.save_data()
        
        
        
        
        
        