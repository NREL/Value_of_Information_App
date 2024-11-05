---
title: 'Value of Information: A Streamlit Python for geothermal exploration'
tags:
  - Decision Analysis
  - Bayesian statistics
  - Python

authors:
  - name: Whitney J. Trainor-Guitton
    orcid: 0000-0002-5726-3886
    equal-contrib: true
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
    name: Karthik Menon (Author Without ORCID)
    equal-contrib: false # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Sierra Rosario (Author Without ORCID)
    equal-contrib: false # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  # - name: Author with no affiliation
  #   corresponding: true # (This is how to denote the corresponding author)
  #   affiliation: 3
  # - given-names: Ludwig
  #   dropping-particle: van
  #   surname: Beethoven
  #   affiliation: 3
affiliations:
 - name: National Renewable Energy Laboratory, USA
   index: 1
 - name: Amherst University, USA
   index: 2
#  - name: Independent Researcher, Country
#    index: 3
date: November 2024
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
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
by quantifying their reliability and how it may help or hinder with decisions. 
VOI is from field of decision analysis and assess if the information will
improve the average outcome of a decision made under uncertainty, like
developing a hidden geothermal resource.

# Statement of need

Many geoscientists working in geothermal do not actively code.  
`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.

# Mathematics

The prior probability $Pr(\Theta = \theta_i)$ where there are two $\theta_i)$:  $i ={negative, positve}$

Double dollars make self-standing equations:

$$Pr( \Theta = \theta_i | X =x_j ) = \color{cyan} \frac{Pr(\Theta = \theta_i ) 
\color{purple} Pr( X=x_j | \Theta = \theta_i )}{\color{orange} Pr (X=x_j)}$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Sierra Rosado during the genesis of this project.

# References
Howard, R. a. (1966). Information Value Theory. <i>Systems Science and Cybernetics, IEEE Transactions On</i>, <i>2</i>(1), 22–26. https://doi.org/10.1109/TSSC.1966.300074