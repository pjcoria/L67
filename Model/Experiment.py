# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 10:39:55 2024

@author: Laboratorio
"""

import numpy as np
import threading
import time
import os
import yaml
import threading
from Model.RP import RP
from datetime import datetime

#%%

class Experiment:
    def __init__(self, config_file):
        self.config_file = config_file
        self.scan_data=[[0],[0]]
        self.is_running = False
        
    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
    
    def load_RP(self):
        self.RP = RP(self.config['RP']['IP'])
    
    def do_scan(self):
        if self.is_running:
            #print('Scan already running')
            return
        self.keep_running = True
        self.is_running = True
        self.RP.set_DF(self.config['Scan']['DF'])
        self.RP.set_trigger(self.config['Scan']['T_source'], self.config['Scan']['T_level'], self.config['Scan']['T_delay'])
        self.RP.measure(self.config['Scan']['M_source'], self.config['Scan']['N_sample'])
        self.scan_data[0] = self.RP.x
        self.scan_data[1] = self.RP.data
        self.is_running = False
        if not self.keep_running:
            return
        
    def start_scan(self):
        self.scan_thread = threading.Thread(target=self.do_scan)
        self.scan_thread.start()
        
    def stop_scan(self):
        self.keep_running = False
        
    def save_data(self):
        data_folder = self.config['Saving']['folder']
        today_folder = f'{datetime.today():%Y-%m-%d}'
        saving_folder = os.path.join(data_folder, today_folder)
        if not os.path.isdir(saving_folder):
            os.makedirs(saving_folder)
        
        data = np.vstack([self.scan_data[0],self.scan_data[1]]).T
        header = 'Tiempo [s], Voltaje [V]'
        
        filename = self.config['Saving']['filename']
        base_name = filename.split('.')[0]
        ext = filename.split('.')[-1]
        i = 1
        while os.path.isfile(os.path.join(saving_folder, f'{base_name}_{i:04d}.{ext}')):
            i += 1
        data_file = os.path.join(saving_folder, f'{base_name}_{i:04d}.{ext}')
        metadata_file = os.path.join(saving_folder, f'{base_name}_{i:04d}_metadata.yml')
        
        np.savetxt(data_file, data, header=header)
        with open(metadata_file, 'w') as f:
            f.write(yaml.dump(self.config, default_flow_style=False))
    
    def finalize(self):
        self.RP.finalize()
    


