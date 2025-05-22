---
title: "Value of Information: A Streamlit Python for geothermal exploration"
tags:
  - Decision Analysis
  - Bayesian statistics
  - Python
authors:
  - name: Whitney J. Trainor-Guitton
  - name: Karthik Menon
affiliations:
  - name: National Renewable Energy Laboratory, USA
    index: 1
date: November 2024
bibliography: paper.bib
---  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
# Summary
  
The Geothermal VOI App reveals which data types best distinguish between a 
hidden conventional geothermal resource and no geothermal resource. Hidden 
geothermal resources are geothermal resources that do not show any evidence
of existence on the surface, thus geophysical and geological observations 
are used to make estimates of subsurface conditions. None of the the data 
layers are direct evidence of heat, permeability and fluids, therefore 
they are imperect indicators [@faulds_discovering_2015]. The value of information (VOI) metric 
attempts to quantify how useful specific information types are
by quantifying their reliability and how it may help or hinder with decisions [@howard_information_1966]. 
VOI is from the field of decision analysis and assess if the information will
improve the average outcome of a decision made under uncertainty, like
developing a hidden geothermal resource.
  
# Statement of need
  
Many geoscientists working in geothermal do not actively code and those outside 
of oil and gas are not familiar with decision analysis. This VOI Streamlit
 App allows geoscientists to visualize the distribution of their data and calculate
 the value of imperfect (real!) data simply by upload two comma-seperated value (.csv) files. 
 These two files represent calibrated data set: data assosciated with a positive and negative hidden geothermal
  sites, respectively.
  
# Mathematics
  
Decision Analysis requires an analysis of the expected outcome (e.g. weighted average) 
of the decision without further information. This uses the probabilities of positive <img src="https://latex.codecogs.com/gif.latex?Pr(\Theta%20=%20positive)"/> and negative <img src="https://latex.codecogs.com/gif.latex?Pr(\Theta%20=%20negative)"/>
hidden geothermal as the weights multiplied by the value outcomes: <img src="https://latex.codecogs.com/gif.latex?v_a(\Theta%20=%20\theta_i)"/>, the values input into the two by two table that typically represent dollar amounts.  <br />
 <img src="https://latex.codecogs.com/gif.latex?V_{prior}%20=%20\max\limits_a%20\sum_i^2%20Pr(\Theta%20=%20\theta_i)%20v_a(\Theta%20=%20\theta_i)"/>
  
Also calculated is the Value with Perfect Information:  <br />
 <img src="https://latex.codecogs.com/gif.latex?V_{perfect}%20=%20\sum_i^2%20Pr(\Theta%20=%20\theta_i)%20\max\limits_a%20v_a(\Theta%20=%20\theta_i)"/>
  <!-- \Sigma_{i=1}^2 Pr(\Theta = \theta_i) \max\limits_a v_a(\theta_i) \ \  \forall a  -->
comparing to <img src="https://latex.codecogs.com/gif.latex?V_{prior}"/> gives an upper bound on what *any* information could bring or the value *of* perfect information (<img src="https://latex.codecogs.com/gif.latex?VOI_{perfect}"/>): \
<img src="https://latex.codecogs.com/gif.latex?VOI_{perfect}%20=%20V_{perfect}-%20V_{prior}"/>
  
After the .csv files are uploaded, the code base performs a grid search on bin sizes (<img src="https://latex.codecogs.com/gif.latex?x_j"/>) or kde bandwidths, as documented in @trainor-guitton_voi_2023. To determine the "best" bandwidth, the data are split into training and testing sets, and the accuracy of Naïve Bayes classifier is evaluated . The grid search performs the Naïve Bayes classification for 20 different bandwidths then compares the predicted class with the true class.  The bandwidth that results in the highest accuracy in Naïve Bayes is deemed the ideal bandwidth.
  
Next, the VOI App calculates the posterior probability: 
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?Pr(%20\Theta%20=%20\theta_i%20|%20X%20=x_j%20)%20=%20\color{cyan}%20\frac{Pr(\Theta%20=%20\theta_i%20)%20\color{purple}%20Pr(%20X=x_j%20|%20\Theta%20=%20\theta_i%20)}{\color{orange}%20Pr%20(X=x_j)}"/></p>  
 \
which scales the "ideal" likelihood from the grid search with the user-entered prior probability of success (<img src="https://latex.codecogs.com/gif.latex?\Theta%20=%20\theta_i"/>).
The posterior replaces the prior to become the weight in the value *with* imperfect information: \
<img src="https://latex.codecogs.com/gif.latex?V_{imperfect}%20=%20\sum_{j=1}^2%20Pr(X%20=%20x_j)%20\max_a%20\sum_{i=1}^2%20%20Pr(\Theta%20=%20\theta_i%20|%20X=x_j)%20%20v_a(\Theta%20=%20\theta_i)"/>
  
This value tells user the ceiling of worth for this data attribute, given the economics and prior probability entered, and the reliability of the data to discriminate between a positive and negative geothermal case.
  
# Example Output 
The demo problem allows users to build intuition on how <img src="https://latex.codecogs.com/gif.latex?V_{prior}"/> and <img src="https://latex.codecogs.com/gif.latex?V_{perfect}"/>.
  
This figure provides a visual example of the empirical likelihood (bars) of the electrical conductivity assosciated with 
positive sites (green) and negative sites (red): 
![Likelihoods of Electrical Conductivity of Lower Crust for INGENIOUS area.\label{fig:Likelihood_CondLowCrust}](Likelihood_CondLowCrust.png )
  
The continuous lines in \autoref{fig:Likelihood_CondLowCrust.png} are the fitted kde likelihoods of the optimal bandwidth given the grid search for accuracy in Naïve Bayes. The likelihood scaled to a prior probability of success (<img src="https://latex.codecogs.com/gif.latex?Pr(\Theta%20=%20positive"/>)=0.2) 
![Prior-Scaled Likelihoods of Electrical Conductivity of Lower Crust for INGENIOUS area.\label{fig:Scaled20Likelihood_CondLowCrust}](Scaled20Likelihood_CondLowCrust.png )
  
The posterior plot of <img src="https://latex.codecogs.com/gif.latex?Pr(\Theta%20=%20positive"/>)=0.2 are shown below
![Posterior of Electrical Conductivity of Lower Crust for INGENIOUS area.\label{fig:Posterior_Prior20}](Posterior_Prior20.png )
This plot shows, given any of the conductivity bin values are observed, how likely are you in a positive (green) versus negative (red) hidden geothermal resource. In general, electrical conductivities of lower crust less than 4.5 (S-m) are more likely to be a negative geothermal site, whereas greater than 4.75 S-m the calibrated dataset show <img src="https://latex.codecogs.com/gif.latex?Pr(\Theta%20=%20positive)"/>= 100%. 
  
# Acknowledgements
We acknowledge contributions from Sierra Rosado during the genesis of this project and from Nicole Taverna for providing feedback. 
We also acknowledge Drew Siler, Andres Laverde, and Gabe Matson for providing case histories using the VOI App for the Geothermal Rising VOI Workshop 2024.
  
# References
 J. E. Faulds et al., “Discovering Blind Geothermal Systems in the Great Basin Region : An Integrated Geologic and Geophysical Approach for Establishing Geothermal Play Fairways,” 2015. [Online]. Available: https://gdr.openei.org/files/756/Faulds-DE-EE0006731-Report-v2.pdf
  
Howard, R. a. (1966). Information Value Theory. <i>Systems Science and Cybernetics, IEEE Transactions On</i>, <i>2</i>(1), 22–26. https://doi.org/10.1109/TSSC.1966.300074
  
Trainor-Guitton, W., & Rosado, S. (2023). A VOI Web Application for Distinct Geothermal Domains: Statistical Evaluation of Different Data Types within the Great Basin. 1836-1851. Paper presented at Geothermal Rising, Reno, Nevada. https://www.geothermal-library.org/index.php?mode=pubs&action=view&record=1034920
  
VanderPlas, Jake. 2016. Python Data Science Handbook: Essential Tools for Working with Data. First edition. Python / Data. Beijing Boston Farnham Sebastopol Tokyo: O’Reilly.
  