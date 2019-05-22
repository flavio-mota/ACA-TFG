#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  22 20:41:47 2019

@author: flaviomota
"""
import random
import numpy as np
from scipy.spatial import distance

def constroi_automato(n, k, estados):
    """
    Função que gera a estrutura do autômato
    
    Parametros
        ----------
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.    
        estados: define quantos valores compõem o estado de cada célula.
    """
    automato = [[[None for j in range(estados)]for j in range(k)]for i in range(n)]
    return automato

def inicializa_estados(A, n, k, v_min, v_max, estados):
    """
    Função que gera os valores dos estados de cada célula do autômato
    através de uma distribução aleatória do valor mínimo e máximo do conjunto 
    de dados
    
    Parametros
        ----------
        A : Autômato Celular de xn. 
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.
        v_min : valor mínimo do conjunto de dados.
        v_max : valor máximo do conjunto de dados.
        estados : quantidade de valores do estado da célula do autômato
    """
    for i in range(n):
        for j in range(k):
            estado = [random.uniform(v_min, v_max) for _ in range(estados)]
            A[i][j] = estado    

def obter_vizinhanca(A, i, j, amostra, tipo, ruido, raio):
    if(tipo == 1): #vizinhança de Moore
        vizinhos_ = []
        for m in range(i-raio,i+raio+1):
            for n in range(j-raio,j+raio+1):
                if(m>=0 and m<len(A) and n>=0 and n<len(A[0])):
                    if(m != i or n != j):
                        vizinhos_.append(escolher_acao(A[m][n],amostra,ruido))
        return vizinhos_
    else: #vizinhança de Von Neumann
        vizinhos_ = []
        for m in range(i-raio,i+raio+1):
            for n in range(j-raio,j+raio+1):
                if(m>=0 and m<len(A) and n>=0 and n<len(A[0])):
                    if(m != i-1 or n != j-1):
                        if(m != i+1 or n != j+1):
                            if(m != i-1 or n != j+1):
                                if(m != i+1 or n != j-1):
                                        if(m != i or n != j):
                                            vizinhos_.append(escolher_acao(A[m][n],amostra,ruido))
        return vizinhos_
                        

def escolher_acao(estado, amostra, ruido):
    return distance.euclidean(estado, amostra)+ruido

def reforco(A, i, j, amostra, eta):
    A[i][j] = A[i][j] + (eta*((amostra) - (A[i][j])))

def agrupar(A, l, c, dados, ruido, eta, probabilidades, grupos, n_iter, raio, max_iter):
    A_ant = np.copy(A)
    convergence = True
    epocas = 0
    estabiliza = 0
    while(convergence and n_iter>0):
        for a in range(len(dados)):
            x = 0
            v_prob = [0.0 for _ in range(l * c)]
            for m in range(l):
                for n in range(c):
                    acoes = []
                    acoes.append(escolher_acao(A[m][n],dados[a], ruido))
                    acoes.append(obter_vizinhanca(A, m, n, dados[a], 1, ruido, raio))
                    if(acoes[0]<min(acoes[1])):
                        reforco(A, m, n, dados[a], eta)
                        grupos[m][n] = 1
                        v_prob[x] = 100 - acoes[0]
                    x +=1
            probabilidades[a] = v_prob
        mudou = False
        for i in range(l):
            for j in range(c):
                if(not(np.array_equal(A[i][j],A_ant[i][j]))):
                    A_ant[i][j] = A[i][j]
                    mudou = True
                    estabiliza = 0
        if(mudou):
            convergence = True
        else:
            estabiliza += 1
        if(estabiliza==max_iter):
            convergence = False
        epocas += 1
        n_iter -= 1

    for i in range(l):
        print (grupos[i])
    print(" ")
    print(epocas)

def mostrar_classes(objetivo, grupos, probabilidades, l, c):
    #Seleciona os rótulos que existem no conjunto e cria um dicionario pra eles
    rotulo = np.unique(objetivo)
    rotulos = {}
    for i in range (len(rotulo)):
        rotulos[rotulo[i]] = 0
    
    x = 0
    for m in range (l):
        for n in range(c):
            if(grupos[m][n] == 1):
                for a in range(len(probabilidades)):
                    m_prob = max(probabilidades[a])
                    if(probabilidades[a].index(m_prob) == x):
                        rotulos[objetivo[a]] += 1
                if(sum(rotulos.values()) > 0):
                    grupos[m][n] = max(rotulos, key = lambda chave: rotulos[chave])
                    for i in range (len(rotulo)):
                        rotulos[rotulo[i]] = 0
            x += 1
    
    for i in range(l):
        print (grupos[i])
    print(" ")
    

def centroides(A, n, k, grupos):
    centroides = []
    for i in range(n):
        for j in range(k):
            if(grupos[i][j]==1):
                centroides.append(A[i][j])
    
    cent = np.unique(np.array(centroides),axis=0)
    return np.asarray(cent)


#def silhueta(dados, centroides, objetivos):
#    labels = []
#    for dado, objetivo in zip(dados, objetivos):
#        distm = None
#        for centro in centroides:
#            dist = (distance.euclidean(dado, centro))
#            if(dist<distm):
                
            