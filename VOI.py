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

def f_VPRIOR(PriorWeight, value_array_mod, *args):  

    """
    Function to calculate the prior value Vprior 

    Parameters
    PriorWeight: array-like [NEG , POS] [1 x 2]
    value_array: array-like [num alternatives x num Geothermal labels] the value array, contains the value outcomes for each possible 
        rows:  do nothing/ drill
        columns: NEGATIVE/POSITIVE 
    cur_value_drill_DRYHOLE : float, optional, change/update value amount for dry hole

    """
    v_array_temp = np.copy(value_array_mod) #Changed here by Karthik to prevent value array from being altered.
    cur_value_drill_DRYHOLE = None 
    for n in args:
      cur_value_drill_DRYHOLE = n

    if cur_value_drill_DRYHOLE is not None:    
        #value_array_mod[1,0] = cur_value_drill_DRYHOLE

        v_array_temp[1,0] = cur_value_drill_DRYHOLE
      
        # Changed here by Karthik on 30 Aug 2024 to reflect profit by reducing drilling cost
        #value_array_mod[1,1] = value_array_mod[1,1] + cur_value_drill_DRYHOLE

        v_array_temp[1,1] = v_array_temp[1,1] + cur_value_drill_DRYHOLE
        

    #print('modified value_array_mod',value_array_mod)    
    prm = PriorWeight #np.hstack((PriorWeight))

    v_a = []
    # st.write('value_array_mod',value_array_mod)
    # Loop over all alternatives : Eventually be Nx * Ny alternatives
    for na in np.arange(0,np.shape(value_array_mod)[0]): # alternatives here are rows...
        #cur_a = np.sum(prm*value_array_mod[na,:])
        cur_a = np.sum(prm*v_array_temp[na,:])
        # st.write('prm, ROW value_array_mod, SUM cur_a',prm,value_array_mod[na,:],cur_a)
        v_a = np.append(v_a, cur_a)

    
    Vprior = np.max(v_a) ; 
    #print('Vprior=', Vprior)
    
    return Vprior

def Vperfect(input_prior, value_array_mod, *args):
    """
    Function to calculate the value with perfect information VPI 

    Parameters
    input_prior: array-like [NEG , POS] [1 x 2]
    value_array_mod: array-like [num alternatives x num of geothermal labels] the value array, contains the value outcomes for each possible 
        geothermal outcome and decision alternative 
        rows:  do nothing/ drill
        columns: NEGATIVE/POSITIVE 
    additional args
    cur_value_drill_DRYHOLE : float, optional, value amount for testing VOI sensitivity
    """

    #Similar change here by Karthik to accomadate drilling costs
    v_array_temp = np.copy(value_array_mod)
    cur_value_drill_DRYHOLE = None 
    for n in args:
      cur_value_drill_DRYHOLE = n

    if cur_value_drill_DRYHOLE is not None:    
        value_array_mod[1,0] = cur_value_drill_DRYHOLE 
        v_array_temp[1,0] = cur_value_drill_DRYHOLE
        v_array_temp[1,1] = v_array_temp[1,1] + cur_value_drill_DRYHOLE
     
    #VPI = np.sum(input_prior * np.max(value_array_mod,0))
    VPI = np.sum(input_prior * np.max(v_array_temp,0))

    return VPI



def f_VIMPERFECT(Prm_d,value_array,Pr_d,*args):
    """
    Function to calculate the highest decision action/alternative (a) given the reliability/posterior of data
    and value_array
    
    Parameters
    Prm_d : array_like, [len(x_sampled) x 2]
        posterior. rows=data space, cols= neg, positive
    value_array : array-like [ 2 x 2]
        the value array, contains the value outcomes for each possible decision alternative (rows)
        a = {drill/nothing}
        columns= label (columns was clay cap) and decision alternative 
    Pr_d : array_like, [len(x_sample) x 1]
        marginal probability, rows= data,
    cur_dryhole_value : float, optional, value amount for testing VOI sensitivity
    """
    cur_value_drill_DRYHOLE = None 
    for n in args:
      cur_value_drill_DRYHOLE = n

    v_aj_array = [] 

    ### If passed, adjust the value array for sensitivity testing. Put new values 
    # in the bottom row, first column and top row, last column
    if cur_value_drill_DRYHOLE is not None: 
        # value_array[-1,0] = cur_value_drill_DRYHOLE
        # value_array[0,-1] = cur_value_drill_DRYHOLE
        value_array[1,0] = cur_value_drill_DRYHOLE 

    v_a = []
    
    # st.write('np.shape(np.exp(Prm_d))',np.shape(np.exp(Prm_d)))
    # st.write('np.exp(Prm_d[0,0]),np.exp(Prm_d[0,-1]',np.exp(Prm_d[0,0]),np.exp(Prm_d[0,-1]))
    # st.write('np.exp(Prm_d[-1,0]),np.exp(Prm_d[-1,-1])',np.exp(Prm_d[-1,0]),np.exp(Prm_d[-1,-1]))
    # st.pyplot(plt.hist(Prm_d))

    ## # Loop through Interpretation bins ~X (columns of Prm_d)
    #for nl in np.arange(0, num_layers):
    v_aj = []
    for j in range(0,np.shape(Prm_d)[0]): #rows=data space, cols= neg, positive
        v_a = []
        ### v_a0 = PrmVul_d[:,j] * x_iVula0  + PrmComp_d[j] * x_iCompa0 
        #print('j: get average',j)
        for a in range(0,np.shape(value_array)[0]):  
            #   [(1 of N) array]  * [1 * M array]
            v_i= sum(Prm_d[j] * value_array[a,:]) # Prm_d: [neg,pos] v_a row: one action at a time
            #if j >90:
            #    print('Prm_d, v_a, (v_i) ', np.exp(Prm_d[j]), value_array[a,:], v_i)
            
            v_a = np.append(v_a, v_i)
        v_aj = np.append(v_aj, np.max(v_a))
    
    v_aj_array = np.append(v_aj_array,v_aj,axis=0)
    # st.write('v_aj_array',np.max(v_aj_array))
    # st.dataframe(Pr_d * v_aj_array)

    # VII:  Value WITH imperfect information
    # print('np.shape(Pr_d) np.sum(Pr_d)',np.shape(Pr_d), np.sum(Pr_d))
    # print(Pr_d[-10:])      
    VII = np.sum(Pr_d * v_aj_array)

    return VII

def f_MI(Prm_d,Pr_d,*args):
    """
    Function to calculate the mutual information: 
    Parameters
    Prm_d : array_like, [len(x_sampled) x 2]
        posterior. rows=data space, cols= neg, positive
    
    Pr_d : array_like, [len(x_sample) x 1]
        marginal probability, rows= data,

    Output:
        Mutual Information (MI) is an information theoretic measure that quantifies how dependent are the two labelings. 
            Note that the maximum value of MI for perfect labelings depends on the number of clusters and samples;
        Normalized Mutual Information (NMI), a Mutual Information defined between 0 (no mutual information) in the limit
            of large number of data points and 1 (perfectly matching label assignments, up to a permutation of the labels). 
            It is not adjusted for chance: then the number of clustered data points is not large enough, the expected values
            of MI or NMI for random labelings can be significantly non-zero;
    """
    MI_post = metrics.mutual_info_score(Prm_d[:,0],Prm_d[:,1])
    NMI_post = metrics.normalized_mutual_info_score(Prm_d[:,0],Prm_d[:,1])

    return MI_post, NMI_post