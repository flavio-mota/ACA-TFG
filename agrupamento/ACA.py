#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  22 20:41:47 2019

@author: flaviomota
"""
import random
import numpy as np
from scipy.spatial import distance

def constroi_automato(x, y, estados):
    """
    Função que gera a estrutura do autômato
    
    Parametros
        ----------
        x : inteiro que define a quantidade de linhas da grade.
        y : inteiro que define a quantidade de colunas da grade.    
        estados: define quantos valores compõem o estado de cada célula.
    """
    automato = [[[None for j in range(estados)]for j in range(y)]for i in range(x)]
    return automato

def inicializa_estados(A, x, y, v_min, v_max, estados):
    """
    Função que gera os valores dos estados de cada célula do autômato
    através de uma distribução aleatória do valor mínimo e máximo do conjunto 
    de dados
    
    Parametros
        ----------
        A : Autômato Celular de xn. 
        x : inteiro que define a quantidade de linhas da grade.
        y : inteiro que define a quantidade de colunas da grade.
        v_min : valor mínimo do conjunto de dados.
        v_max : valor máximo do conjunto de dados.
        estados : quantidade de valores do estado da célula do autômato
    """
    for i in range(x):
        for j in range(y):
            estado = [random.uniform(v_min, v_max) for _ in range(estados)]
            A[i][j] = estado    

def obter_vizinhanca(A, i, j, amostra, tipo, ruido):
    if(tipo == 1): #vizinhança de Moore
        if(j == 0):
            if(i == 0):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j+1], amostra, ruido))
                return vizinhos_acao
            if((i != 0) and ( i!= (len(A)-1))):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j+1], amostra, ruido))            
                return vizinhos_acao
            if(i == (len(A)-1)):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j+1], amostra, ruido))
                return vizinhos_acao
        if((j!=0) and (j != (len(A)-1))):
            if(i == 0):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j+1], amostra, ruido))                
                return vizinhos_acao
            if((i != 0) and ( i!= (len(A)-1))):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j+1], amostra, ruido))
                return vizinhos_acao
            if(i == (len(A)-1)):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i][j+1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j+1], amostra, ruido))
                return vizinhos_acao
        if(j == (len(A)-1)):
            if(i == 0):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j-1], amostra, ruido))
                return vizinhos_acao
            if((i!=0) and(i!=(len(A)-1))):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j-1], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i+1][j-1], amostra, ruido))
                return vizinhos_acao
            if(i == (len(A)-1)):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i-1][j], amostra, ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1], amostra, ruido))   
                vizinhos_acao.append(escolher_acao(A[i-1][j-1], amostra, ruido))
                return vizinhos_acao
    else: #vizinhança de Von Neumann
        if(j == 0):
            if(i == 0):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1],amostra,ruido))
                return vizinhos_acao
            if((i != 0) and ( i!= (len(A)-1))):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j],amostra,ruido))
                return vizinhos_acao
            if(i == (len(A)-1)):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i][j+1],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j],amostra,ruido))
                return vizinhos_acao
        if((j!=0) and (j != (len(A)-1))):
            if(i == 0):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1],amostra,ruido))
                return vizinhos_acao
            if((i != 0) and ( i!= (len(A)-1))):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j+1],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1],amostra,ruido))
                return vizinhos_acao
            if(i == (len(A)-1)):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i][j+1],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1],amostra,ruido))
                return vizinhos_acao
        if(j == (len(A)-1)):
            if(i == 0):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1],amostra,ruido))
                return vizinhos_acao
            if((i!=0) and(i!=(len(A)-1))):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i+1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i-1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1],amostra,ruido))
                return vizinhos_acao
            if(i == (len(A)-1)):
                vizinhos_acao = []
                vizinhos_acao.append(escolher_acao(A[i-1][j],amostra,ruido))
                vizinhos_acao.append(escolher_acao(A[i][j-1],amostra,ruido))
                return vizinhos_acao

def escolher_acao(estado, amostra, ruido):
    return distance.euclidean(estado, amostra)+ruido

def reforco(A, i, j, amostra, eta):
    A[i][j] = A[i][j] + np.array(eta*(np.array(amostra) - np.array(A[i][j])))

def agrupar(A, l, c, dados, ruido, eta, probabilidades, grupos):
    for _ in range(10):
        for a in range(len(dados)):
            x = 0
            v_prob = [0.0 for _ in range(l * c)]
            for m in range(l):
                for n in range(c):
                    acoes = []
                    acoes.append(escolher_acao(A[m][n],dados[a], ruido))
                    acoes.append(obter_vizinhanca(A, m, n, dados[a], 1, ruido))
                    if(acoes[0]<min(acoes[1])):
                        reforco(A, m, n, dados[a], eta)
                        grupos[m][n] = 1
                        v_prob[x] = 100 - acoes[0]
                    x +=1
            probabilidades[a] = v_prob
    
    for i in range(l):
        print (grupos[i])
    print(" ")

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
    
def similaridade(A, grupos, l, c):
    distancias = {}
    for i in range(l):
        for j in range(c):
            rotulo = grupos[i][j]
            if(rotulo != None):
                for m in range(l):
                    for n in range(c):
                        if((grupos[m][n] != None) and (grupos[m][n] != rotulo)):
                            distancias[str(rotulo)+','+str(grupos[m][n])] = distance.euclidean(A[i][j], A[m][n])
    return distancias