#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  23 16:14:34 2019

@author: flaviomota
"""

import random
import numpy as np

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

A, classes_ = constroi_automato(3, 5, 4, ['setosa', 'versicolor', 'virginica'])
inicializa_estados(A, 3, 5, 0.1, 7.9, 4)

print(acoes(A, 3, 5, [5.1, 3.5, 1.4, 0.2], 0))
    