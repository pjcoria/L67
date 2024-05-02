# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:29:21 2024

@author: Laboratorio
"""

from PyQt5.QtWidgets import QApplication
from Model.Experiment import Experiment 
from View.main_window_ import MainWindow

#%%

exp=Experiment('experiment.yml')
exp.load_config()
exp.load_RP()

app = QApplication([])
win = MainWindow(exp)

win.show()
app.exec()
