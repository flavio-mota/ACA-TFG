#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  22 20:41:47 2019

@author: flaviomota
"""
import ACA as ac
from sklearn import datasets


"""
----------PARAMÊTROS
"""
iris = datasets.load_iris() #carrega o dataset IRIS
dados = iris.data #extrai os valores de cada atributo
objetivo = iris.target

l = 3 #define quantidade de linhas
c = 3 #define quantidade de colunas    
estados = len(dados[0]) #extrai quantos valores de estados serão necessários
ruido = 0.1 #ruído da função de escolha de ação
eta = 0.1 #taxa de aprendizagem
v_min = 0.1 #valor mínimo do conjunto de dados
v_max = 7.9 #valor máximo do conjunto de dados
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
probabilidades = [' ' for _ in range(len(objetivo))]

#APRENDIZAGEM DO AUTÔMATO
ac.agrupar(A, l, c, dados, ruido, eta, probabilidades, grupos)

ac.mostrar_classes(objetivo, grupos, probabilidades, l, c)

