# Value of Information (VOI) Streamlit App 

## Installation

Install the package and dependencies:

```
pip install -e .
```

## Running Locally

```
streamlit run app.py --server.enableXsrfProtection false 
```

## Value of Information parameters
Users are able to model a "drill or walk away" decision and input prior probability of geothermal resource existing. Prior Value and Value of Perfect Information are ouput.

Next, the value of imperfect information is calculated, using a dataframe from various geophysical and geologicial observations around known geothermals systems and other locations deemed not a geothermal resource ("negative").

## Working Examples
User's can run a jupyternotebook using the following link: https://mybinder.org/v2/gh/NREL/Value_of_Information_App/354ccb5114849dd8004c24748bf49c24c07afce9?urlpath=lab%2Ftree%2Fsample_jupyternotebook.ipynb
Alternatively, they are free to use the online streamlit app as well: https://voigeothermalrising.streamlit.app/

## Format of .csv files

You must upload one .csv file with data assosciated with positive label and one file with data assosciated with negative labels. **Both** must contain at a minimum a column labeled for the distance to the label: "PosSite_Distance" and "NegSite_Distance" resepectively.

Examples are shown [here](https://github.com/wtrainor/INGENIOUS_streamlit/tree/main/File%20Template)

NREL Software Record number SWR-25-15.
