import math
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KernelDensity
from sklearn.naive_bayes import GaussianNB
import os
import io

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import GridSearchCV
from sklearn import metrics 

class KDEClassifier(BaseEstimator, ClassifierMixin):
    """Bayesian generative classification based on KDE

    Parameters
    ----------
    bandwidth : float
        the kernel bandwidth within each class
    kernel : str
        the kernel name, passed to KernelDensity
    """
    def __init__(self, bandwidth=1.0, kernel='gaussian'):
        self.bandwidth = bandwidth
        self.kernel = kernel

    def fit(self, X, y):
        self.classes_ = np.sort(np.unique(y))
        training_sets = [X[y == yi] for yi in self.classes_]
        self.models_ = [KernelDensity(bandwidth=self.bandwidth,
                                      kernel=self.kernel).fit(Xi)
                        for Xi in training_sets]
        self.logpriors_ = [np.log(Xi.shape[0] / X.shape[0])
                           for Xi in training_sets]
        #st.write('self.logpriors_',self.logpriors_)
        return self

    def predict_proba(self, X):
        logprobs = np.array([model.score_samples(X)
                             for model in self.models_]).T
        result = np.exp(logprobs + self.logpriors_)
        return result / result.sum(1, keepdims=True)

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), 1)]

def make_train_test(dfpair,x_cur,dfpairN):
    """
    Function to split up data into training and test sections. Only the training part is fed into optimal bin calculation.

    dfpair : pandas dataframe  [len(data in POSITIVE .csv) x 1]
        data that associated with positive label
    x_cur : str
        data attribute chosen by user
    dfpairN : pandas dataframe  [len(data in NEGATIVE .csv) x 1]
        data that are associated with negative label

    returns
         X_train, y_train [(number of data points)*0.80 x 1]
         X_test, y_test [(number of data points)*0.20 x 1]
    """
    X_all = pd.concat((dfpair[x_cur],dfpairN[x_cur]))
    
    # Labels 
    y_g = np.ones((1, dfpair.shape[0]))
    y_all = np.append(y_g,(np.zeros((1, dfpairN.shape[0]))))
    
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
    
    return  X_train, X_test, y_train, y_test 

def optimal_bin(X_train, y_train):
    """
    Function that uses grid search and Naive Bayes classification to determine optimal bin size
    X_train : array_like, 
        Nrows = [number of data points]*0.67
        Ncolumns = number of features (current implementation is one at a time)
    y_train : labels attached to each data point

    Returns are "best parameters" which includes bin size for one feature
    """
    
    x_d = np.linspace(min(X_train), max(X_train), 100)
    
    maxValue = x_d[-1]
    range_div20 = (maxValue - x_d[0])/20.0; #st.write('range_div20 ',range_div20 )
   
    bandwidths = np.linspace(range_div20  , maxValue/3.0, 40) # was max value of attribute. not useful
    
    grid = GridSearchCV(KDEClassifier(), {'bandwidth': bandwidths})

    X_train_np = X_train.values
    #st.write(X_train.iloc[0:5], X_train_np[0:3])
    grid.fit(X_train_np[:,None],y_train) # removed  [:,None],  .to_numpy() doesn't work np.reshape(,(-1,1)), y_train
    scores = grid.cv_results_['mean_test_score']
    # st.write(grid.best_params_)
    # st.write('accuracy =', grid.best_score_)

    return grid.best_params_,  grid.best_score_