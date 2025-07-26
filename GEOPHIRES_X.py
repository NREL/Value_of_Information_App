from geophires_x_client import GeophiresXClient
from geophires_x_client.geophires_input_parameters import GeophiresInputParameters
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import colors 
from matplotlib import ticker
import os
from PIL import Image
import requests
from io import BytesIO

def Geophires_output(gradient,depth,type_geo,no_prod,no_inj):
    client = GeophiresXClient()
    result = client.get_geophires_result(
                GeophiresInputParameters({
                    "Gradient 1": gradient,
                    "Reservoir Depth": depth,
                    "End-Use Option": type_geo,
                    # "Power Plant Type": "1", #subcritical ORC, had "3" originally
                    "Economic Model": "3",
                    "Starting Electricity Sale Price": "0.15",
                    "Ending Electricity Sale Price": "1.00",

                    #"Reservoir Heat Capacity": "790",
                    #"Reservoir Thermal Conductivity": "3.05",
                    #"Reservoir Porosity": "0.0118",
                    #"Reservoir Impedance": "0.01",
                    #"Number of Fractures": "108",
                    #"Fracture Shape": "4",
                    #"Fracture Height": "300",
                    #"Fracture Width": "400",
                    #"Fracture Separation": "30",
                    "Number of Production Wells": no_prod,
                    "Number of Injection Wells": no_inj, #Keep out for now, add in later
                })
            )



    with open(result.output_file_path, 'r') as f:
    #print(f.read())
    #print(f.read(1500))
        words = ['Project NPV:','Drilling and completion costs per well:']
                    
        lines = f.readlines()
                            
        num = 30            
        # Manually setting since parsing is not working

        #for row1 in range(len(lines)):
            ## check if string present on a current line
            #row = lines[row1]
            #st.write(row)
            #word = 'Project NPV:'
            
            #print(row.find(word))
            # find() method returns -1 if the value is not found,
            # if found it returns index of the first occurrence of the substring
            #if row.find(word) != -1:
                #st.write('string exists in file')
                #st.write('line Number:', lines.index(row))
                #no = lines.index(row)
                #no = row1

        
        npv = str(lines[num-1:num]) # Drilling and completion costs
        npv1= npv.split(':')
        npv1 = npv.replace(" ","")
        npv1 = npv1.replace('\n',"")
        npv1 = npv1.split('MUSD')
        
        npv2 = npv1[0:1]
        
        npv2 = str(npv2)
        npvv = npv2.split(':')
        final_npv = npvv[1:2]
        aa = str(final_npv[0:1])
        val = (''.join(c for c in aa if (c.isdigit() or c =='.' or c =='-')))
        val2 = (val.strip())
    
        val2 = float(val2)

        
        npv_final = val2*1e6
        

        num = 31            
        # Manually setting since word is not working
        #for row1 in range(len(lines)):
            ## check if string present on a current line
            #row = lines[row1]
            #st.write(row)
            #word = 'Project NPV:'
            
            #print(row.find(word))
            # find() method returns -1 if the value is not found,
            # if found it returns index of the first occurrence of the substring
            #if row.find(word) != -1:
                #st.write('string exists in file')
                #st.write('line Number:', lines.index(row))
                #no = lines.index(row)
                #no = row1

        # For drilling cost
        
        num = 93 # Change to 95 in new one


        npv = str(lines[num-1:num]) # Drilling and completion costs per well
        print('npv line 112', npv)
        npv1= npv.split(':')
        npv1 = npv.replace(" ","")
        npv1 = npv1.replace('\n',"")
        npv1 = npv1.split('MUSD')
        
        npv2 = npv1[0:1]
        
        npv2 = str(npv2)
        npvv = npv2.split(':')
        final_npv = npvv[1:2]
        aa = str(final_npv[0:1])
        val = (''.join(c for c in aa if (c.isdigit() or c =='.' or c =='-')))
        val2 = (val.strip())
        val2 = float(val2)
        drill_cost = -1*val2*1e6

        num = 94
        npv = str(lines[num-1:num]) # Drilling and completion costs
    
        npv1= npv.split(':')
        npv1 = npv.replace(" ","")
        npv1 = npv1.replace('\n',"")
        npv1 = npv1.split('MUSD')
        
        npv2 = npv1[0:1]
        
        npv2 = str(npv2)
        npvv = npv2.split(':')
        final_npv = npvv[1:2]
        aa = str(final_npv[0:1])
        val = (''.join(c for c in aa if (c.isdigit() or c =='.' or c =='-')))
        val2 = (val.strip())

        val2 = float(val2)
        drill_cost2 = -1*val2*1e6
        
        
    
    
    if (type_geo == 2):
        drill_cost = drill_cost2
    else:
        drill_cost = drill_cost
        
    return npv_final,drill_cost