#%% Importamos librerias
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
#%% Cargamos los datos

path = 'D:\\Exactas\\Laboratorio_VI_VII\\L67\\Mediciones_fotodiodo\\650nm'
ext = '.csv'
txt_files = [i for i in os.listdir(path) if os.path.splitext(i)[1] == ext]
data_dict={}
for file in txt_files:
    data_dict[file] = {'data' :[[],[]]}
    data_dict[file]['data'][0], data_dict[file]['data'][1] = np.loadtxt(path + '\\' + file, skiprows=1, unpack=True)
    data_dict[file]['data'][0] = np.array(data_dict[file]['data'][0])
    data_dict[file]['data'][1] = np.array(data_dict[file]['data'][1])


#%% Graficamos todas las series de datos y calculamos la tensión maxima registrada en promedio

maxs=[]
pots=[]

for idx, file in enumerate (data_dict.keys()):
    ymax = data_dict[file]['data'][1][40:].max()
    #ymax_index = np.where(data_dict[file]['data'][1] == ymax)[0][0]
    ymax_index_min = np.where(2.0<(data_dict[file]['data'][0]*1000000))[0]
    ymax_index_max = np.where(data_dict[file]['data'][0]*1000000<3)[0]
    y_range = np.intersect1d(ymax_index_min, ymax_index_max, assume_unique=False, return_indices=False)
    ymax_mean = data_dict[file]['data'][1][y_range[0]:y_range[-1]].mean()
    maxs.append(ymax_mean)
    pots.append(float(file[6:9].replace(',', '.')))
    plt.Figure()
    plt.title(file)
    plt.plot(data_dict[file]['data'][0][40:]*1000000, data_dict[file]['data'][1][40:]*1000)
    plt.plot(data_dict[file]['data'][0][y_range[0]:y_range[-1]]*1000000, data_dict[file]['data'][1][y_range[0]:y_range[-1]]*1000, color='r')
    plt.xlabel('Tiempo [us]')
    plt.ylabel('Tension [mV]')
    plt.grid()
    plt.show()

#%% Calculamos y graficamos la tension maxima registrada en funcion de la potencia del laser

def f(x,a,b):
    return a*x+b

popt, pcov = curve_fit(f, pots, maxs)
x = np.linspace(pots[0],pots[-1],100)

plt.figure()
plt.title('Voltaje maximo adquirido en funcion de la potencia recibida')
plt.scatter(pots,maxs)
plt.grid()
plt.xlabel('Potencia [uW]')
plt.ylabel('Voltaje maximo promedio [mV]')
plt.plot(x,f(x,*popt), linestyle='--', color='r', label=f'Ajuste lineal, a={round(popt[0],4)}, b={round(popt[1],4)}')
plt.legend()
plt.show()
