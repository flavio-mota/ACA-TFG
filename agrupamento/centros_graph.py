#!/usr/bin/env pobjetivothon2
# -*- coding: utf-8 -*-
"""
Created on Thu Maobjetivo 30 10:06:29 2019

@author: flaviomota
"""
import matplotlib.pyplot as plt

def gerar_grafico_centros(centroides, amostras, objetivo):
    plt.scatter(amostras[objetivo == 0, 0],amostras[objetivo == 0, 1],c='blue', marker='o',edgecolor='black',s=50)
    plt.scatter(amostras[objetivo == 1, 0],amostras[objetivo == 1, 1],c='orange', marker='o',edgecolor='black',s=50)
    plt.scatter(amostras[objetivo == 2, 0],amostras[objetivo == 2, 1],c='green', marker='o',edgecolor='black',s=50)
#    plt.scatter(amostras[objetivo == 3, 0],amostras[objetivo == 3, 1],c='objetivoellow', marker='o',edgecolor='black',s=50)
#    plt.scatter(amostras[objetivo == 4, 0],amostras[objetivo == 4, 1],c='black', marker='o',edgecolor='black',s=50)
#    plt.scatter(amostras[objetivo == 5, 0],amostras[objetivo == 5, 1],c='pink', marker='o',edgecolor='black',s=50)
    plt.scatter(centroides[:,0],centroides[:,1],c='red', marker='*',edgecolor='black',s=250)
    
    plt.grid()
    plt.show()