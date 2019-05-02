#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  23 16:14:34 2019

@author: flaviomota
"""

import random
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

def constroi_automato(n, k, estados, classes):
    """
    Função que gera a estrutura do autômato
    
    Parametros
        ----------
        n : inteiro que define a quantidade de linhas da grade. Está relacionado 
            diretamente com a quantidade de classes.
        k : inteiro que define a quantidade de colunas da grade.    
        estados: define quantos valores compõem o estado de cada célula.
        classes: define os nomes das classes para cada classificador.
    """
    automato = [[[None for j in range(estados)]for j in range(k)]for i in range(n)]
    classes_ = []
    for i in classes:
        classes_.append(i);
    return automato, classes_

def inicializa_estados(A, n, k, v_min, v_max, estados):
    """
    Função que gera os valores dos estados de cada célula do autômato
    através de uma distribução aleatória do valor mínimo e máximo do conjunto 
    de dados
    
    Parametros
        ----------
        A : Autômato Celular de nk. 
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

def acoes(A, n, k, amostra, ruido):
    acoes_ = [[None for j in range(k)]for i in range(n)]
    for i in range(n):
        for j in range(k):
            acoes_[i][j] = escolher_acao(A[i][j], amostra, ruido)
    return acoes_
    
def escolher_acao(estado, amostra, ruido):
    return 1 if np.dot(estado,amostra) + ruido > 0 else -1

def atualiza_estado(A, reforco, acao, eta, b, amostra, i, j):
    if(reforco == 1):
        A[i][j] = A[i][j] + eta*(np.dot(A[i][j],amostra) - (reforco*acao))*amostra
    if(reforco == -1):
        A[i][j] = A[i][j] + b*eta*(np.dot(A[i][j],amostra) - (reforco*acao))*amostra
        
def vizinhanca(acoes_, i, j, raio, k):
    l = 1
    vizinhos_ = []
    while(l<=raio and j-l>=0):
        vizinhos_.append(acoes_[i][j-l])
        l+=1
    l = 1
    while(l<=raio and j+l<=k-1):
        vizinhos_.append(acoes_[i][j+l])
        l+=1
    return vizinhos_

def treinamento(A, n, k, dados_treinamento, ruido, raio, eta, b):
    dados = dados_treinamento['dados']
    objetivos = dados_treinamento['objetivo']
    for amostra, objetivo in zip(dados, objetivos):
        classe_X = objetivo 
        acoes_ = acoes(A, n, k, amostra, ruido)
        for i in range(n):
            for j in range(k):
                if(classes_[i] == classe_X):
                    if(acoes_[i][j] == 1):
                        vizinhos_ = vizinhanca(acoes_, i, j, raio, k)
                        if(vizinhos_.count(1) >= (len(vizinhos_)/2)):
                            atualiza_estado(A, 1, 1, eta, b, amostra, i, j)
                        else:
                            atualiza_estado(A, -1, 1, eta, b, amostra, i, j)
                    else:
                        atualiza_estado(A, -1, -1, eta, b, amostra, i, j)
                else:
                    if(acoes_[i][j]==-1):
                        vizinhos_ = vizinhanca(acoes_, i, j, raio, k)
                        if(vizinhos_.count(-1) >= (len(vizinhos_)/2)):
                            atualiza_estado(A, 1, -1, eta, b, amostra, i, j)
                        else:
                            atualiza_estado(A, -1, -1, eta, b, amostra, i, j)
                    else:
                        atualiza_estado(A, -1, 1, eta, b, amostra, i, j)

def teste(A, n, k, dados_teste, ruido):
    dados = dados_teste['dados']
    objetivos = dados_teste['objetivo']
    for amostra, objetivo in zip(dados,objetivos):
        acoes_ = acoes(A, n, k, amostra, ruido)
        for i in range(n):
            if(i==objetivo):
                


A, classes_ = constroi_automato(3, 20, 4, [0,1,2])
inicializa_estados(A, 3, 20, 0.1, 7.9, 4)
print(A)

iris = datasets.load_iris() #carrega o dataset IRIS
dados = iris.data #extrai os valores de cada atributo
y = iris.target


X_train, X_test, y_train, y_test = train_test_split(dados, y, 
                                    test_size = 0.3, random_state = 1, stratify=y)

dados_treinamento = {'dados': X_train, 'objetivo': y_train}

treinamento(A,3,20,dados_treinamento, 0.2, 5, 1, 1)



    