#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  22 20:41:47 2019

@author: flaviomota
"""
import ACA as ac
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.metrics import cluster


"""
----------PARÂMETROS
"""
#iris = datasets.load_iris() #carrega o dataset IRIS
#dados = iris.data #extrai os valores de cada atributo
#objetivo = iris.target
#
#X, y = datasets.make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5,
#                           shuffle=True, random_state=0)

#X, y = datasets.make_moons(n_samples=200,
#                           noise=.05,
#                           random_state=0)

X, y=  datasets.make_circles(n_samples=700, factor=.5,
                                      noise=.05)

l = 5 #define quantidade de linhas
c = 5 #define quantidade de colunas    
estados = 2 #extrai quantos valores de estados serão necessários
ruido = 0.1 #ruído da função de escolha de ação
eta = 0.1 #taxa de aprendizagem
v_min = -1 #valor mínimo do conjunto de dados
v_max = 1 #valor máximo do conjunto de dado
n_iter = 100 #número de iterações
raio = 2 #vizinhança que será analisada
max_iter = 15 #número máximo para convergência
"""
------------------------------
"""

#construção do autômato
A = ac.constroi_automato(l,c,estados)

#inicializar os estados
ac.inicializa_estados(A, l, c, v_min, v_max, estados) 

#Vetor de probabilidade
probabilidades = [' ' for _ in range(len(y))]

#APRENDIZAGEM DO AUTÔMATO
centroides, rotulos, y_aca = ac.agrupar(A, l, c, X, y, ruido, eta, probabilidades, n_iter, raio, max_iter)

print('Rand: ', cluster.adjusted_rand_score(y, y_aca))

plt.scatter(X[y == 0, 0],X[y == 0, 1],c='blue', marker='o',edgecolor='black',s=50)
plt.scatter(X[y == 1, 0],X[y == 1, 1],c='green', marker='o',edgecolor='black',s=50)
plt.scatter(X[y == 2, 0],X[y == 2, 1],c='orange', marker='o',edgecolor='black',s=50)
#plt.scatter(X[y == 3, 0],X[y == 3, 1],c='yellow', marker='o',edgecolor='black',s=50)
#plt.scatter(X[y == 4, 0],X[y == 4, 1],c='black', marker='o',edgecolor='black',s=50)
#plt.scatter(X[y == 5, 0],X[y == 5, 1],c='pink', marker='o',edgecolor='black',s=50)
plt.scatter(centroides[:,0],centroides[:,1],c='red', marker='*',edgecolor='black',s=250)

plt.grid()
plt.show()
#ac.mostrar_classes(objetivo, grupos, probabilidades, l, c)

#print(ac.similaridade(A, grupos, l, c))

