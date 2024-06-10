#%% Importamos librerias
import matplotlib.pyplot as plt
import numpy as np
import os
#%% Cargamos los datos
path = 'D:\\Exactas\\Laboratorio_VI_VII\\L67\\Mediciones_fotodiodo\\650nm'

data_dict = {'650nm-0,7uW-OD5,2.csv': {'data' :[[],[]]}, '650nm-1,2uW-OD4,9.csv': {'data' :[[],[]]}, '650nm-1,3uW-OD4,7.csv': {'data' :[[],[]]},
           '650nm-1,8uW-OD4,5.csv': {'data' :[[],[]]}, '650nm-4,6uW-OD4,0.csv': {'data' :[[],[]]}, '650nm-5,0uW-OD3,8.csv': {'data' :[[],[]]},
           '650nm-6,2uW-OD3,7.csv': {'data' :[[],[]]}, '650nm-7,1uW-OD3,6.csv': {'data' :[[],[]]}, '650nm-7,3uW-OD3,5.csv': {'data' :[[],[]]},
           '650nm-8,6uW-OD3,4.csv': {'data' :[[],[]]}}

for file in data_dict.keys():
    data_dict[file]['data'][0], data_dict[file]['data'][1] = np.loadtxt(path+ '\\' +file, skiprows=1, unpack=True)
    data_dict[file]['data'][0] = np.array(data_dict[file]['data'][0])
    data_dict[file]['data'][1] = np.array(data_dict[file]['data'][1])

#%% Graficamos todas las series de datos

for idx, file in enumerate (data_dict.keys()):
    plt.Figure()
    plt.title(file)
    plt.plot(data_dict[file]['data'][0][40:]*1000000, data_dict[file]['data'][1][40:]*1000)
    plt.xlabel('Tiempo [us]')
    plt.ylabel('Tension [mV]')
    plt.grid()
    plt.show()


#%% Calculamos y graficamos la tension maxima registrada en funcion de la potencia del laser

maxs=[]
pots=[]

for file in data_dict.keys():
    ymax = data_dict[file]['data'][1][40:].max()
    ymax_index = np.where(data_dict[file]['data'][1]==ymax)[0][0]
    ymax_mean = data_dict[file]['data'][1][ymax_index-20:ymax_index+20].mean()
    maxs.append(ymax_mean)
    pots.append(float(file[6:9].replace(',','.')))

plt.figure()
plt.scatter(pots,maxs)
plt.show()
