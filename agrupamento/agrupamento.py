#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  22 20:41:47 2019

@author: flaviomota
"""
import ACA as ac
import centros_graph as cg
import silhueta_graph as sg
from sklearn import datasets
from sklearn.metrics import cluster
from sklearn.cluster import KMeans
import numpy as np

"""
----------PARÂMETROS
"""
#iris = datasets.load_iris() #carrega o dataset IRIS
#dados = iris.data #extrai os valores de cada atributo
#objetivo = iris.target
##
#X, y = datasets.make_blobs(n_samples=50, n_features=2, centers=3, cluster_std=0.2,
#                           shuffle=True, random_state=0)

X, y = datasets.make_moons(n_samples=200,
                           noise=.05,
                           random_state=0)
#
#X, y=  datasets.make_circles(n_samples=700, factor=.5,
#                                      noise=.05)

l = 5 #define quantidade de linhas
c = 5 #define quantidade de colunas    
estados = 2 #extrai quantos valores de estados serão necessários
ruido = 0.1 #ruído da função de escolha de ação
eta = 0.1 #taxa de aprendizagem
v_min = np.min(X) #valor mínimo do conjunto de dados
v_max = np.max(X) #valor máximo do conjunto de dado
n_iter = 100 #número de iterações
raio = 2 #vizinhança que será analisada
max_iter = 15 #número máximo para convergência
"""
------------------------------
"""
centroides_ = []
rand_score_ = []
silhueta_score_ = []
epocas_ = []
rand_score_km_ = []
silhueta_score_km_ = []

iter = 10
while(iter>0):
    #construção do autômato
    A = ac.constroi_automato(l,c,estados)
    
    #inicializar os estados
    ac.inicializa_estados(A, l, c, v_min, v_max, estados) 
    
    #Vetor de probabilidade
    probabilidades = [' ' for _ in range(len(y))]
    
    #APRENDIZAGEM DO AUTÔMATO
    centroides, rotulos, y_aca, epocas = ac.agrupar(A, l, c, X, y, ruido, eta, probabilidades, n_iter, raio, max_iter)
    
    centroides_.append(centroides)
    epocas_.append(epocas)
    rand_score_.append(cluster.adjusted_rand_score(y, y_aca))
    
    silhueta_score_.append(cluster.silhouette_score(X,y_aca, metric='euclidean'))
    
    n_clusters = len(centroides)

    km = KMeans(n_clusters = n_clusters,
                init = 'random',
                n_init = 10,
                max_iter = 300,
                tol=1e-04,
                random_state = 0)
    y_km = km.fit_predict(X)
    
    rand_score_km_.append(cluster.adjusted_rand_score(y, y_km))
    silhueta_score_km_.append(cluster.silhouette_score(X,y_km, metric='euclidean'))
    
    iter -= 1


#cg.gerar_grafico_centros(centroides, X, y)
#cg.gerar_grafico_centros(km.cluster_centers_, X, y)
print('centros: ', centroides_)
print('epocas: ', np.mean(epocas_))
print('indice rand: ', np.mean(rand_score_))
print('indice silhueta: ', np.mean(silhueta_score_))
print('indice rand kmeans: ', np.mean(rand_score_km_))
print('indice silhueta kmeans: ', np.mean(silhueta_score_km_))
#sg.gerar_grafico_silhueta(X, y_aca)

#ac.mostrar_classes(objetivo, grupos, probabilidades, l, c)

#print(ac.similaridade(A, grupos, l, c))

