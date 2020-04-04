# -*- coding: utf-8 -*-
"""
Example script for processing and plotting GLM data
The script uses the data of an oscillation task performed with the 
manipulandum (file TEST_DATA.glm)

Created on Wed Jan 29 11:16:06 2020

@author: opsomerl & fschiltz
"""
#%% Importation des librairies necessaires
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

import glm_data_processing as glm
import derive as der
import Add 

# Fermeture des figures ouvertes
plt.close('all') 
donnees_accX = [[],[],[],[]] # haut avec, haut sans, bas avec, bas sans
donnees_GF = [[],[],[],[]] 
donnees_LF = [[],[],[],[]]  
donnees_dGF = [[],[],[],[]] 
to_cancel = [[],[],[],[]]
delai = [[],[],[],[]]

file=os.listdir("mesures") 
subjects=[path.split('_')[0]+'_'+path.split('_')[1]+'_'+path.split('_')[2] for i,path in enumerate(file) if i%3 == 0] 
  
# Double for-loop that runs through all subjects and trials 
def make_plots(beginning,The_end,Name='alex',Delai=False,add=False,zoom=False,chock_number=1,Trial=0):
    global donnees_accX, donnees_GF, donnees_LF, donnees_dGF, to_cancel, subjects
    subjects = subjects[beginning:The_end]
    if zoom and (not add) and (not Delai): 
        subjects = [subjects]         
    for s in subjects:
        name,hb,block = s.split('_')[:3] 
        for trial in range(1,4): 
            if trial==Trial or Trial==0:
                # Set data path
                glm_path = "mesures/%s_00%d.glm" % (s,trial)
                
                # Import data 
                glm_df = glm.import_data(glm_path)
                
                baseline = range(0,400)        
                # Normal Force exerted by the thumb
                NF_thumb = glm_df.loc[:,'Fygl']-np.nanmean(glm_df.loc[baseline,'Fygl'])
                # Vertical Tangential Force exerted by the thumb
                TFx_thumb  = glm_df.loc[:,'Fxgl']-np.nanmean(glm_df.loc[baseline,'Fxgl'])
                #Horizontal Tangential Force exerted by the thumb
                TFz_thumb  = glm_df.loc[:,'Fzgl']-np.nanmean(glm_df.loc[baseline,'Fzgl'])
         
                # Normal Force exerted by the index
                NF_index = -(glm_df.loc[:,'Fygr']-np.nanmean(glm_df.loc[baseline,'Fygr']))
                # Vertical Tangential Force exerted by the index
                TFx_index = glm_df.loc[:,'Fxgr']-np.nanmean(glm_df.loc[baseline,'Fxgr'])
                #Horizontal Tangential Force exerted by the index
                TFz_index = glm_df.loc[:,'Fzgr']-np.nanmean(glm_df.loc[baseline,'Fzgr'])
                 
                #%% Get acceleration, LF and GF
                time  = glm_df.loc[:,'time'].to_numpy()
                accX  = glm_df.loc[:,'LowAcc_X'].to_numpy()*(-9.81)
                accX  = accX-np.nanmean(accX[baseline])
                GF    = glm_df.loc[:,'GF'].to_numpy()
                GF    = GF-np.nanmean(GF[baseline])
                LFv   = TFx_thumb+TFx_index
                LFh   = TFz_thumb+TFz_index
                LF    = np.hypot(LFv,LFh)
                
                # %%Filter data
                freqAcq=800 #Frequence d'acquisition des donnees
                freqFiltAcc=20 #Frequence de coupure de l'acceleration
                freqFiltForces=20 #Frequence de coupure des forces
                  
                accX = glm.filter_signal(accX, fs = freqAcq, fc = freqFiltAcc)
                GF   = glm.filter_signal(GF,   fs = freqAcq, fc = freqFiltForces)
                LF   = glm.filter_signal(LF,   fs = freqAcq, fc = freqFiltForces)
                LFv   = glm.filter_signal(LFv,   fs = freqAcq, fc = freqFiltForces)
                LFh   = glm.filter_signal(LFh,   fs = freqAcq, fc = freqFiltForces)
                
                #%% CUTTING THE TASK INTO SEGMENTS (your first task)
                pk = signal.find_peaks(abs(accX),prominence=9,distance=2000) # avant:prominence=9,distance=1000
                ipk = pk[0][0:10]
                
                if ipk[-1]-ipk[-2]>9000*0.8:
                    ipk = ipk[:9] 
                     
                cycle_starts = ipk-400  # 1 seconde = 800 
                cycle_ends = ipk+800
                
                start = time[cycle_starts[chock_number-1]] 
                end = time[cycle_ends[chock_number-1]] 
                       
                #%% Compute derivative of LF
                dGF=der.derive(GF,800)
                dGF=glm.filter_signal(dGF, fs = freqAcq, fc = 10)
                #%% Basic plot of the data 
                fig = None ; ax = None
                if zoom and (not add) and (not Delai):
                    fig = plt.figure(figsize = [3,12]) 
                elif (not add) and (not Delai):
                    fig = plt.figure(figsize = [15,7])
                if add or Delai:  
                    if hb == 'haut': 
                        if block == 'avec':
                            donnees_accX[0].append([accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[0].append([GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[0].append([LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[0].append([dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            to_cancel[0].append([])  
                        elif block == 'sans':
                            donnees_accX[1].append([accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[1].append([GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[1].append([LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[1].append([dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)])  
                            to_cancel[1].append([])    
                    elif hb == 'bas':
                        if block == 'avec':
                            donnees_accX[2].append([accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[2].append([GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[2].append([LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[2].append([dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            to_cancel[2].append([])     
                        elif block == 'sans':
                            donnees_accX[3].append([accX[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_GF[3].append([GF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_LF[3].append([LF[st:e] for st,e in zip(cycle_starts,cycle_ends)]) 
                            donnees_dGF[3].append([dGF[st:e] for st,e in zip(cycle_starts,cycle_ends)])  
                            to_cancel[3].append([])    
                else:    
                    ax  = fig.subplots(3,1) 
                    
                    ax[0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
                    ax[0].set_title("Simple example of GLM data", fontsize=14, fontweight="bold")
                   
                    ax[1].set_xlabel("Time [s]", fontsize=13)
                    ax[1].set_ylabel("Forces [N]", fontsize=13)
                    
                    ax[2].set_xlabel("Time [s]", fontsize=13)
                    ax[2].set_ylabel("GF derivative [N/s]", fontsize=13)
                    
                    ax[0].plot(time, accX)
                    ax[0].plot(time[ipk],accX[ipk], linestyle='', marker='o', 
                           markerfacecolor='None', markeredgecolor='r')
                    ax[1].plot(time,LF, label="LF")
                    ax[1].plot(time,GF, label="GF")
                    ax[1].legend(fontsize=12)
                    ax[2].plot(time,dGF)
                    if zoom:
                        ax[0].set_xlim([start,end])
                        ax[1].set_xlim([start,end])
                        ax[2].set_xlim([start,end])
                        mini = accX[ipk[chock_number-1]]
                        ax[0].set_ylim([mini-2,-mini]) 
                    else:
                        ax[0].set_xlim([0,time[ipk[-1]+3200]])
                        ax[1].set_xlim([0,time[ipk[-1]+3200]])
                        ax[2].set_xlim([0,time[ipk[-1]+3200]]) 
                    
                if (not zoom) and (not add) and (not Delai):
                    # Putting grey patches for cycles
                    for i in range(0,len(cycle_starts)):
                        rect0=plt.Rectangle((time[cycle_starts[i]],ax[0].get_ylim()[0]),\
                                           time[cycle_ends[i]-cycle_starts[i]],\
                                           ax[0].get_ylim()[1]-ax[0].get_ylim()[0],color='k',alpha=0.3)
                        ax[0].add_patch(rect0)
                    
                #%% Save the figure as png file. Creates a folder "figures" first if it
                # doesn't exist
                if not fig==None:
                    if not os.path.exists('figures'):
                        os.makedirs('figures')
                    
                    fig.savefig("figures\%s_%d_acc_forces_dGF.png" %(s,trial)) 
                    
    if add:
        Add.superpose(Name,to_cancel,donnees_accX,donnees_GF,donnees_LF,donnees_dGF)
    elif Delai:
        Add.delai(Name)                                               