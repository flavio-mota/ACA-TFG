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
    
    Parâmetros
        ----------
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.    
        estados : inteiro que define quantos valores compõem o estado de uma célula.
    
    Retorno
        ----------
        automato : estrutura do autômato.
    """
    automato = [[[None for j in range(estados)]for j in range(k)]for i in range(n)]
    return automato

def inicializa_estados(A, n, k, v_min, v_max, estados):
    """
    Função que inicializa os valores dos estados de cada célula do autômato
    através de uma distribução aleatória de um valor mínimo e máximo
    
    Parâmetros
        ----------
        A : Autômato Celular de nk. 
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.
        v_min : inteiro/decimal que define o valor mínimo.
        v_max : inteiro/decimal que define o valor máximo.
        estados : inteiro que define quantos valores compõem o estado de uma célula.
    """
    for i in range(n):
        for j in range(k):
            estado = [random.uniform(v_min, v_max) for _ in range(estados)]
            A[i][j] = estado    

def obter_vizinhanca(A, i, j, amostra, tipo, ruido, raio):
    """
    Função que obtém as ações dos vizinhos de uma determinada célula.
    
    Parâmetros
        ----------
        A : Autômato Celular de nk.
        i : inteiro que define a posição da célula na linha.
        j : inteiro que define a posição da célula na grade.    
        amostra : vetor com o dados apresentados às células.
        tipo : inteiro que determina qual o tipo de vizinhança a ser utilizada,
                podendo ser Moore (1) ou Von Neumann(2).
        ruido : decimal que é utilizado no cálculo da ação.
        raio : inteiro que determina quantos níveis de vizinhos devem ser visitados.
    
    Retorno
        ----------
        vizinhos_ : vetor contendo as ações dos vizinhos de uma determinada célula.
    """
    if(tipo == 1): #vizinhança de Moore
        vizinhos_ = []
        for m in range(i-raio,i+raio+1):
            for n in range(j-raio,j+raio+1):
                if(m>=0 and m<len(A) and n>=0 and n<len(A[0])):
                    if(m != i or n != j):
                        vizinhos_.append(escolher_acao(A[m][n],amostra,ruido))
        return vizinhos_
    if(tipo == 2): #vizinhança de Von Neumann
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
    """
    Função que determina a ação de uma célula.
    
    Parâmetros
        ----------
        estado : vetor com o estado atual da célula.
        amostra : vetor com o dados apresentados à célula.
        ruido : decimal que é utilizado no cálculo da ação.
    
    Retorno
        ----------
        Distância euclidiana entre dois pontos somada ao ruído.
    """
    return distance.euclidean(estado, amostra)+ruido

def reforco(A, i, j, amostra, eta):
    """
    Função que aplica o reforço em uma determinada célula, atualizando seu estado.
    
    Parâmetros
        ----------
        A : Autômato Celular de nk.
        i : inteiro que define a posição da célula na linha.
        j : inteiro que define a posição da célula na grade.    
        amostra : vetor com o dados apresentados às células.
        eta : decimal que determina a taxa de aprendizagem.
    
    """
    A[i][j] = A[i][j] + (eta*((amostra) - (A[i][j])))
    
def centroides(A, n, k, grupos):
    """
    Função que determina os protótipos dos centróides do agrupamento.
    
    Parâmetros
        ----------
        A : Autômato Celular de nk.
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.    
        grupos : matriz contendo um indicador de que a célula mudou de estado
                 durante o processo de aprendizagem, sinalizado um centro.
    
    Retorno
        ----------
        Matriz contendo os centróides gerados pelo agrupamento.
    """
    centroides = []
    for i in range(n):
        for j in range(k):
            if(grupos[i][j]==1):
                centroides.append(A[i][j])
    
    
    cent = np.unique(np.array(centroides),axis=0)

#TODO analisar a implementação de um 'merge' dos centróides próximos    
#    cent_ = []
#    for atual in cent:
#        prox_ = []
#        for centro in cent:
#            if(distance.euclidean(atual, centro) < 1.0):
#                prox_.append(centro)
#        if(len(prox_)>0):        
#            estado = np.mean(prox_, axis=0)
#            cent_.append(estado)
#        else:
#            cent_.append(atual)
        
    return np.asarray(cent)

def rotular(A, n, k, amostras, objetivos, centroides_):
    """
    Função que determina o rótulo de cada grupo e de cada amostra de dado.
    
    Parâmetros
        ----------
        A : Autômato Celular de nk.
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.    
        amostras : matriz contendo o conjunto de dados agrupados.
        objetivos : vetor contendo o rótulo real de cada dado.
        centroides_ : vetor contendo os centróides gerados.
    
    Retorno
        ----------
        rotulos : dicionário contendo os rótulos de cada grupo.
        y_aca : vetor contendo os rótulos gerados para cada dado.
    """
    rotulos = {}
    for i in range(len(centroides_)):
        rotulos[i] = 0
    
    i = 0
    for centro in centroides_:
        distancias = []
        for dado in amostras:
            distancias.append(distance.euclidean(centro, dado))
        rotulo = objetivos[distancias.index(min(distancias))]
        rotulos[i] = rotulo
        i+=1
    
    y_aca = []
    
    for dado in amostras:
        min_dist = distance.euclidean(centroides_[0], dado)
        i, ind = 0, 0
        for centro in centroides_:
            if(distance.euclidean(centro, dado) < min_dist):
                min_dist = distance.euclidean(centro, dado)
                ind = i
            i+=1
        y_aca.append(rotulos[ind])
                
    return rotulos, y_aca

def agrupar(A, l, c, dados, objetivos, ruido, eta, probabilidades, n_iter, raio, max_iter):
    """
    Função que realiza o agrupamento.
    
    Parâmetros
        ----------
        A : Autômato Celular de nk.
        l : inteiro que define a quantidade de linhas da grade.
        c : inteiro que define a quantidade de colunas da grade.    
        dados : matriz contendo o conjunto de dados a serem agrupados.
        objetivos : vetor contendo o rótulo real de cada dado.
        ruido : decimal que é utilizado no cálculo da ação.
        eta : decimal que determina a taxa de aprendizagem.
        probabilidades : estrutura de vetor para armazenar as probabilidades 
                         de um dado rotulado pertencer a uma célula.
        n_iter : inteiro que define o número máximo de iterações do processo de agrupamento.
        aio : inteiro que determina quantos níveis de vizinhos devem ser visitados.
        max_iter : inteiro que determina o número máximo de iterações onde os estados não mudam (estabilidade).
    
    Retorno
        ----------
        centroides_ : matriz contendo os centróides gerados pelo agrupamento.
        rotulos : dicionário contendo os rótulos de cada grupo.
        y_aca : vetor contendo os rótulos gerados para cada dado.
    """
    grupos = constroi_automato(l,c,1)
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

    
    centroides_ = centroides(A,l,c,grupos)

    rotulos, y_aca = rotular(A,l,c,dados,objetivos,centroides_)
    
    return centroides_, rotulos, y_aca, epocas

#TODO analisar a necessidade dessa função (remover!)
def mostrar_classes(objetivo, grupos, probabilidades, l, c):
    """
    Função que mostra o rótulo dos grupos criados para dados rotulados.
    
    Parâmetros
        ----------
        objetivo : vetor contendo o rótulo real de cada dado.
        grupos : matriz contendo o sinalizador de que uma célula participou do
                 processo de agrupamento.
        probabilidades : vetor que armazena a probabilidade de um dado rotulado 
                         pertencer a uma célula.
        l : inteiro que define a quantidade de linhas da grade.
        c : inteiro que define a quantidade de colunas da grade.
        
    """    
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
    



#def silhueta(dados, centroides, objetivos):
#    labels = []
#    for dado, objetivo in zip(dados, objetivos):
#        distm = None
#        for centro in centroides:
#            dist = (distance.euclidean(dado, centro))
#            if(dist<distm):
                
            