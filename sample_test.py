import pytest

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import ticker
import os
import io
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import requests



from User_input import st_file_selector, Prior_probability_binary, make_value_array
from Naive_Bayes import make_train_test, optimal_bin
from Bayesian_Modeling import likelihood_KDE, Scaledlikelihood_KDE, Posterior_by_hand, Posterior_Marginal_plot, marginal, Posterior_via_NaiveBayes
from VOI import Vperfect, f_MI, f_VIMPERFECT, f_VPRIOR


def Prior():
    pro = Prior_probability_binary()
    return pro

def psum(prior):
    url = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\POS_Walker_INGENIOUS.csv"
    #pos_file = requests.get(url).content


    url1 = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\NEG_Walker_INGENIOUS.csv"
    #neg_file = requests.get(url).content
    df = pd.read_csv(url)

    dfN = pd.read_csv(url1)
    attribute  = df.columns[7] # Randomly choosing one. If the use wishes to choose one manually, change the code here

    df_sc = df[df[attribute]>-9999]
    df_scN = dfN[dfN[attribute]>-9999]
    dist_met = np.max(df_sc['PosSite_Distance'].quantile(0.1)) # Can change here as well
    dist_met = 800

    dfpair00 = df_sc[(df_sc['PosSite_Distance'] <=round(dist_met,-1))] 
    neg_site_col_name = 'NegSite_Distance'        
    dfpair = dfpair00[dfpair00[attribute]>-9999] 
    # # # OJO : may want to keep this off until have it for NEG 
    dfpairN = df_scN[(df_scN[neg_site_col_name] <=round(dist_met,-1))] 
    if np.shape(dfpairN)[0]==0:
        dfpairN = df_scN[(df_scN[neg_site_col_name ] <= np.percentile(df_scN[neg_site_col_name ],10))] 

    X_train, X_test, y_train, y_test = make_train_test(dfpair,attribute,dfpairN)
 
    best_params, accuracy = optimal_bin(X_train, y_train)
    predictedLikelihood_pos, predictedLikelihood_neg, x_sampled, count_ij= likelihood_KDE(X_train,X_test, y_train, y_test,attribute, best_params)

    pos_like_sum = np.sum(predictedLikelihood_pos)
    neg_like_sum = np.sum(predictedLikelihood_neg)

    # Default Prior
    Pr_prior_POS = prior
    Pr_InputMarg, Pr_UnifMarg, Prm_d_Input, Prm_d_Uniform = Posterior_by_hand(Pr_prior_POS,predictedLikelihood_pos, predictedLikelihood_neg, x_sampled)

    marg_sum = np.sum(Pr_InputMarg)
    
    return (pos_like_sum + neg_like_sum + marg_sum)

def dist1():
    url = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\POS_Walker_INGENIOUS.csv"
    #pos_file = requests.get(url).content


    url1 = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\NEG_Walker_INGENIOUS.csv"
    #neg_file = requests.get(url).content
    df = pd.read_csv(url)

    dfN = pd.read_csv(url1)

    pos = df['PosSite_Distance'].min()
    neg = dfN['NegSite_Distance'].min()

    return pos

def dist2():
    url = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\POS_Walker_INGENIOUS.csv"
    #pos_file = requests.get(url).content


    url1 = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\NEG_Walker_INGENIOUS.csv"
    #neg_file = requests.get(url).content
    df = pd.read_csv(url)

    dfN = pd.read_csv(url1)

    pos = df['PosSite_Distance'].min()
    neg = dfN['NegSite_Distance'].min()

    return neg

def VOI(prior):

    Pr_prior_POS = prior
    url = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\POS_Walker_INGENIOUS.csv"
    #pos_file = requests.get(url).content


    url1 = "C:\\Users\\kmenon\\Documents\\INGENIOUS_Data\\Actual_INGENIOUS_csvs_for_AOI_App\\NEG_Walker_INGENIOUS.csv"
    #neg_file = requests.get(url).content
    df = pd.read_csv(url)

    dfN = pd.read_csv(url1)
    attribute  = df.columns[7] # Randomly choosing one. If the use wishes to choose one manually, change the code here

    df_sc = df[df[attribute]>-9999]
    df_scN = dfN[dfN[attribute]>-9999]
    dist_met = np.max(df_sc['PosSite_Distance'].quantile(0.1)) # Can change here as well
    dist_met = 800

    dfpair00 = df_sc[(df_sc['PosSite_Distance'] <=round(dist_met,-1))] 
    neg_site_col_name = 'NegSite_Distance'        
    dfpair = dfpair00[dfpair00[attribute]>-9999] 
    # # # OJO : may want to keep this off until have it for NEG 
    dfpairN = df_scN[(df_scN[neg_site_col_name] <=round(dist_met,-1))] 
    if np.shape(dfpairN)[0]==0:
        dfpairN = df_scN[(df_scN[neg_site_col_name ] <= np.percentile(df_scN[neg_site_col_name ],10))] 

    X_train, X_test, y_train, y_test = make_train_test(dfpair,attribute,dfpairN)
 
    best_params, accuracy = optimal_bin(X_train, y_train)
    predictedLikelihood_pos, predictedLikelihood_neg, x_sampled, count_ij= likelihood_KDE(X_train,X_test, y_train, y_test,attribute, best_params)
    Pr_InputMarg, Pr_UnifMarg, Prm_d_Input, Prm_d_Uniform = Posterior_by_hand(Pr_prior_POS,predictedLikelihood_pos, predictedLikelihood_neg, x_sampled)
    pos_drill_outcome = 1e7
    neg_drill_outcome = -1e7
    value_array, value_array_df = make_value_array(count_ij, profit_drill_pos= pos_drill_outcome, cost_drill_neg = neg_drill_outcome)

        
                        

    

    VPI = Vperfect(Pr_prior_POS, value_array)
            
            
            
    VII_input = f_VIMPERFECT(Prm_d_Input, value_array, Pr_InputMarg)
    VII_unifPrior = f_VIMPERFECT(Prm_d_Uniform, value_array, Pr_UnifMarg)
    return (VPI- VII_input)


def test_function():
    # (3-psum(Prior_probability_binary())) <= 0
    # prior() <= 1
    assert VOI(Prior_probability_binary()) >= 0 


def test_function2():
    # (3-psum(Prior_probability_binary())) <= 0
    # prior() <= 1
    assert (3-psum(Prior_probability_binary())) <= 0


def test_function3():
    # (3-psum(Prior_probability_binary())) <= 0
    # prior() <= 1
    assert Prior() <= 1

def test_function4():
# (3-psum(Prior_probability_binary())) <= 0
# prior() <= 1
    assert (dist1() >= 0 and dist2() >= 0)