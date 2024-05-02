# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:08:37 2024

@author: Laboratorio
"""
import matplotlib.pyplot as plt
import numpy as np
import time
from Controller import redpitaya_scpi as scpi
#%%
class RP:
    def __init__(self,ip):
        self.IP=ip
        self.driver=scpi.scpi(self.IP)
        self.dformat='ASCII'
        self.units='VOLTS'
        self.data=[0]
        self.x=np.arange(0,8191,1)
        self.DF=1
        self.max_SR=125000000
        
    def __str__(self):
        self.driver.tx_txt('SYSTem:BRD:Name?')
        return f'Red Pitaya (Model: {self.driver.rx_txt()})'
        
    def initialize(self):
        self.driver.tx_txt('ACQ:RST')
        self.driver.tx_txt(f'ACQ:DATA:FORMAT {self.dformat}')
        self.driver.tx_txt(f'ACQ:DATA:Units {self.units}')
        
    def set_trigger(self,source,level,delay):
        self.driver.tx_txt(f'ACQ:TRig:LEV {level} V')
        self.driver.tx_txt(f'ACQ:TRig:DLY:NS {delay}')
        self.driver.tx_txt(f'ACQ:TRig {source}')
        
    def get_trigger(self):
        self.driver.tx_txt('ACQ:TRig:LEV?')
        print(f'Trigger level: {self.driver.rx_txt()}')
        self.driver.tx_txt('ACQ:TRig:DLY:NS?')
        print(f'Trigger delay in ns: {self.driver.rx_txt()}')
        self.driver.tx_txt('')
        #Por el momento no hay un comando SCPI para preguntar la fuente del trigger
        
    def set_DF(self,DF):
        self.DF=DF
        self.driver.tx_txt(f'ACQ:DEC {self.DF}')
        
    def get_DF(self):
        self.driver.tx_txt('ACQ:DEC?')
        print(f'Decimation factor: {self.driver.rx_txt()}')
        
# Se podría agregar una función para medir todo el buffer incluyendo un sleep para que no incluya basura      
    def measure(self,source,n):
        self.driver.tx_txt('ACQ:START')
        while 1:
            self.driver.tx_txt('ACQ:TRIG:STAT?')
            if self.driver.rx_txt() == 'TD':
                break
        while 1:
            self.driver.tx_txt('ACQ:TRIG:FILL?')
            if self.driver.rx_txt() == '1':
                break
        self.driver.tx_txt(f'ACQ:{source}:DATA?')
        buff_string = self.driver.rx_txt()
        buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
        self.data = list(map(float, buff_string))
        self.driver.tx_txt('ACQ:STOP')
        self.x=np.arange(0,n*(self.DF/self.max_SR),self.DF/self.max_SR)
        self.data=self.data[8192:8192+n]
    def finalize(self):
        self.driver.tx_txt('ACQ:STOP')
        self.driver.tx_txt('ACQ:RST')
        
#%%

if __name__=='__main__':
    rp=RP('rp-f04df7.local')
    rp.initialize()
    rp.set_DF(4)
    rp.set_trigger('NOW', 0.5, 0)
    rp.measure('SOUR1',700)
    plt.scatter(rp.x*1000000,rp.data)
    plt.xlabel('Tiempo[us]')
    plt.ylabel('Voltaje [V]')
    plt.grid()

