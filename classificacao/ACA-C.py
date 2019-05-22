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
from sklearn.preprocessing import StandardScaler


def constroi_automato(n, k, estados, classes):
    """
    Função que gera a estrutura do autômato
    
    Parametros
        ----------
        n : inteiro que define a quantidade de linhas da grade. Está relacionado 
            diretamente com a quantidade de classes.
        k : inteiro que define a quantidade de colunas da grade.    
        estados: inteiro que define quantos valores compõem o estado de cada célula.
        classes: vetor define os nomes das classes para cada classificador.
    
    Retorno
        ----------
        automato : estrutura do autômato no formato [n][k].
        classes_ : vetor com as n classes a serem encontradas.
    """
    automato = [[[None for j in range(estados)]for j in range(k)]for i in range(n)]
    classes_ = []
    for i in classes:
        classes_.append(i);
    return automato, classes_

def inicializa_estados(A, n, k, v_min, v_max, estados):
    """
    Função que gera os valores dos estados de cada célula do autômato
    através de uma distribução aleatória de um valor mínimo e máximo.
    
    Parametros
        ----------
        A : Autômato Celular de nk. 
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.
        v_min : decimal|inteiro que define o valor mínimo.
        v_max : decimal|inteiro que define o valor máximo.
        estados : inteiro que define a quantidade de valores do estado da célula 
                  do autômato.
    
    Retorno
        ----------
        O autômato com seus estados inicializados.
    """
    for i in range(n):
        for j in range(k):
            estado = [random.uniform(-1, 1) for _ in range(estados)]
            A[i][j] = estado 

def acoes(A, n, k, amostra, ruido):
    """
    Função que cria uma estrutura [n][k] que representa as ações de cada célula
    do autômato, dada uma amostra de dado que é apresentada à todas as células.
    
    Parametros
        ----------
        A : Autômato Celular de nk. 
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.
        amostra : vetor com o dado a ser apresentado a célula.
        ruido : decimal com valor aleatório.
    
    Retorno
        ----------
        acoes_ : estrutura [n][k] com as ações escolhidas por cada célula.
    """
    
    acoes_ = [[None for j in range(k)]for i in range(n)]
    for i in range(n):
        for j in range(k):
            acoes_[i][j] = escolher_acao(A[i][j], amostra, ruido)
    return acoes_
    
def escolher_acao(estado, amostra, ruido):
    """
    Função que calcula a ação de uma célula, considerando o produto interno dos 
    vetores de estado atual e vetor de dados de entrada. Retorna 1 ou -1.
    
    Parametros
        ----------
        estado : vetor que representa o estado atual da célula.
        amostra : vetor com os dados de entrada.
        ruido : decimal com valor aleatório.
    
    Retorno
        ----------
        1 ou -1, dada o cálculo do protudo interno dos vetores somado a um ruído.
    """
    return 1 if np.dot(estado,amostra) + ruido > 0 else -1

def atualiza_estado(A, reforco, acao, eta, b, amostra, i, j):
    """
    Função que atualiza o estado de uma célula do autômato. Se o sinal de reforço
    for 1, recompensa a célula. Se o sinal de reforço for -1, penaliza a célula.
    
    Parametros
        ----------
        A : Autômato Celular de nk.
        reforco : inteiro que determina recompensa ou penalização.
        acao : inteiro que possui o valor da ação escolhida pela célula.
        eta : decimal que representa a taxa de aprendizagem.
        b : decimal que representa a taxa de penalização.
        amostra : vetor com os dados de entrada.
        i : inteiro que determina a linha da célula.
        j : inteiro que determina a coluna da célula.
    
    Retorno
        ----------
        Estado da célula A[i][j] atualizado de acordo com o sinal de reforço.
    """
    if(reforco == 1):
        A[i][j] = A[i][j] + eta*(np.dot(A[i][j],amostra) - (reforco*acao))*amostra
    if(reforco == -1):
        A[i][j] = A[i][j] + b*eta*(np.dot(A[i][j],amostra) - (reforco*acao))*amostra


        
def vizinhanca(acoes_, i, j, raio, k):
    """
    Função que verifica as ações dos vizinhos a direita e a esquerda de uma 
    determinada célula [i][j].
    
    Parametros
        ----------
        acoes_ : vetor que representa as ações escolhidas por cada célula.
        i : inteiro que determina a linha da célula.
        j : inteiro que determina a coluna da célula.
        raio : inteiro que determina o raio da vizinhança da célula, ou seja,
               quantos vizinhos a direita e a esquerda serão analizados.
        k : inteiro que define a quantidade de colunas do autômato.
    
    Retorno
        ----------
        vizinhos_ : vetor contendo os valores de ação dos vizinhos da célula [i][j]
    """
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

#TODO descrever em detalhes o funcionamento da função treinamento 
def treinamento(A, n, k, dados_treinamento, ruido, raio, eta, b, n_iter, classes_):
    """
    Função que treina o Autômato apresentando o conjunto de dados de treinamento 
    escolhido.
    
    Parametros
        ----------
        A : Autômato Celular de nk.
        n : inteiro que define a quantidade de linhas da grade.
        k : inteiro que define a quantidade de colunas da grade.
        dados_treinamento : estrutura que armazena os dados utilizados para o treinamento.
        ruido : decimal com valor aleatório.
        raio : inteiro que determina o raio da vizinhança da célula, ou seja,
               quantos vizinhos a direita e a esquerda serão analizados.
        eta : decimal que representa a taxa de aprendizagem.
        b : decimal que representa a taxa de penalização.
        n_iter : inteiro que define o número de repetições.
        classes_ : vetor com as classes a serem encontradas.
    
    Retorno
        ----------
        Estados do Autômato atualizados e função de ação ajustada.
    """
    while(n_iter>0):
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
                            atualiza_estado(A, -1, 1, eta, b, amostra, i, j)
        n_iter-=1

#TODO descrever a função teste
def teste(A, n, k, dados_teste, ruido):
    dados = dados_teste['dados']
    objetivos = dados_teste['objetivo']
    resultado = []
    for amostra, objetivo in zip(dados,objetivos):
        acoes_ = acoes(A, n, k, amostra, ruido)
        print(objetivo, acoes_)
        votacao_ = []
        for i in range(n):
            votacao_.append(acoes_[i].count(1))
        resultado.append(votacao_.index(max(votacao_)))
    return resultado
                
                


A, classes_ = constroi_automato(3, 20, 13, [0,1,2])

inicializa_estados(A, 3, 20, 0.1, 7.9, 13)


iris = datasets.load_wine() #carrega o dataset IRIS
dados = iris.data #extrai os valores de cada atributo
y = iris.target


X_train, X_test, y_train, y_test = train_test_split(dados, y, 
                                    test_size = 0.1, random_state = 1, stratify=y)
sc = StandardScaler()
sc.fit(X_train)
sc.fit(X_test)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

#for amostra, objetivo in zip(X_train_std, y_train):
#    print('amostra: ', amostra, '/objetivo: ', objetivo)


dados_treinamento = {'dados': np.array(X_train_std), 'objetivo': y_train}
dados_teste = {'dados': X_test_std, 'objetivo': y_test}

print('treinamento: ')
treinamento(A,3,20,dados_treinamento, 1, 5, 0.5, 0, 1, classes_)


resultado = teste(A, 3, 20, dados_teste, 1)
#
for i in range(len(y_test)):
    print(resultado[i], y_test[i])

print((y_test != resultado).sum())    
 