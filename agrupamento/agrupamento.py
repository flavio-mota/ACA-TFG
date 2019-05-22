#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  22 20:41:47 2019

@author: flaviomota
"""
import ACA as ac
from sklearn import datasets
import matplotlib.pyplot as plt



"""
----------PARAMÊTROS
"""
#iris = datasets.load_iris() #carrega o dataset IRIS
#dados = iris.data #extrai os valores de cada atributo
#objetivo = iris.target
#
X, y = datasets.make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, 
                  shuffle=True, random_state=0)
#
#X, y = datasets.make_moons(n_samples=200,
#                           noise=.05,
#                           random_state=0)

l = 4 #define quantidade de linhas
c = 3 #define quantidade de colunas    
estados = 2 #extrai quantos valores de estados serão necessários
ruido = 0.1 #ruído da função de escolha de ação
eta = 0.1 #taxa de aprendizagem
v_min = -1 #valor mínimo do conjunto de dados
v_max = 1 #valor máximo do conjunto de dado
n_iter = 100 #número de iterações
raio = 1 #vizinhança que será analisada
max_iter = 5 #número máximo para convergência
"""
------------------------------
"""

#construção do autômato
A = ac.constroi_automato(l,c,estados)

#inicializar os estados
ac.inicializa_estados(A, l, c, v_min, v_max, estados) 

#matriz que verifica quais células mudaram de estado
grupos = ac.constroi_automato(l,c,1)

#Vetor de probabilidade
probabilidades = [' ' for _ in range(len(y))]

#APRENDIZAGEM DO AUTÔMATO
ac.agrupar(A, l, c, X, ruido, eta, probabilidades, grupos, n_iter, raio, max_iter)

centroides = ac.centroides(A,l,c,grupos)

plt.scatter(X[:,0],X[:,1],c='white', marker='o',edgecolor='black',s=50)
plt.scatter(centroides[:,0],centroides[:,1],c='red', marker='*',edgecolor='black',s=250)
plt.grid()
plt.show()
#ac.mostrar_classes(objetivo, grupos, probabilidades, l, c)

#print(ac.similaridade(A, grupos, l, c))

