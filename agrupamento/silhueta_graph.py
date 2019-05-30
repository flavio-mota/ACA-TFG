#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:11:01 2019

@author: flaviomota
"""

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sklearn.metrics import cluster

def gerar_grafico_silhueta(amostras, y_aca):
    cluster_labels = np.unique(y_aca)
    n_clusters = cluster_labels.shape[0]
    silhouette_vals = cluster.silhouette_samples(amostras,y_aca,metric='euclidean')
    
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []
    for i, c in enumerate(cluster_labels):
        c_silhouette_vals = silhouette_vals[y_aca == c]
        c_silhouette_vals.sort()
        y_ax_upper += len(c_silhouette_vals)
        color = cm.jet(float(i)/n_clusters)
        plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals,
                 height=1.0,
                 edgecolor='none',
                 color=color)
        yticks.append((y_ax_lower+y_ax_upper)/2.)
        y_ax_lower += len(c_silhouette_vals)
    
    silhouette_avg = np.mean(silhouette_vals)
    plt.axvline(silhouette_avg,
                color='red',
                linestyle="--")
    plt.yticks(yticks,cluster_labels+1)
    plt.ylabel('Cluster')
    plt.xlabel('Silhouette coefficient')
    plt.show()