# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:10:40 2020

@author: Dany
"""

import numpy as np

masses = range(1,4)
random_masses = np.random.choice(masses,(12,10))
times = range(4,8)
random_times = np.random.choice(times,(12,9))  
flux = open("random.txt","w")
for k in range(12):
    for j in range(10):
        if j == 0:
            flux.write("Bloc "+str(k)+":   "+"masse"+"\t   "+"temps"+"\n")
            flux.write("\t   "+str(random_masses[k,j])+"\t   "+str(random_times[k,j])+"\n")
        elif j == 9:
            flux.write("\t   "+str(random_masses[k,j])+"\n")
        else:
            flux.write("\t   "+str(random_masses[k,j])+"\t   "+str(random_times[k,j])+"\n")
    flux.write("\n")  
flux.close()      