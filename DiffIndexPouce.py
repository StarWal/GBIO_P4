#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:40:44 2020

@author: alexandreloffet
"""

import numpy as np

import glm_data_processing as glm
#%%
#def utiles
#Retourne la valeur absolue de la difference
def dif(F_index,F_pouce):
    a=np.abs(F_index-F_pouce)
    return a

def MoyIndThumb(F_index,F_pouce):
    i=np.abs(F_index)
    t=np.abs(F_pouce)
    a=(i+t)/2
    return a

#%%
#@F=dans le code de felicien
subjects = ["alex_haut_avec","alex_haut_sans","alex_bas_sans","alex_bas_avec",
            "florent_haut_avec","florent_haut_sans","florent_bas_sans","florent_bas_avec",
            "victor_haut_avec","victor_haut_sans","victor_bas_sans","victor_bas_avec",
            "walid_haut_avec","walid_haut_sans","walid_bas_sans","walid_bas_avec"] #Names of subjects
ntrials = 3 #Number of trials for each subject

subject_number=0;#@F

i=0 #Compteur pour la 1ere boucle for
RatioSujets=[]
RatioMoySujets=[]
ListeNom=["Alexandre","Florent","Victor","Walid"]

flux = open("ratio_FN_pouce_index.txt","w")
flux.write("Feuille pour voir la difference entre la force normale de l index et du pouce"+"\n"+"\n")

for s in subjects:#@F
    for trial in range(1,ntrials+1): #@F
        # Set data path
        glm_path = "%s_00%d.glm" % (s,trial)#@F
        
        # Import data 
        glm_df = glm.import_data(glm_path)#@F
        
        baseline = range(0,400)        #@F
        # Normal Force exerted by the thumb
        NF_thumb = glm_df.loc[:,'Fygl']-np.nanmean(glm_df.loc[baseline,'Fygl'])#@F

        # Normal Force exerted by the index
        NF_index = -(glm_df.loc[:,'Fygr']-np.nanmean(glm_df.loc[baseline,'Fygr']))#@F
        
    #Moyenne des valeurs absolues des différences index-pouce    
    difList=dif(NF_index,NF_thumb)
    moyDif=np.mean(difList)
    
    #Moyenne de la force exercée par le pouce et l'indexx
    IetT=MoyIndThumb(NF_index,NF_thumb)
    moyIetT=np.mean(IetT)
    
    #Moyenne de la force exercee par le pouce
    moyT=np.mean(NF_thumb)
    
    #Moyenne de la force exercee par l index
    moyI=np.mean(NF_index)
    
    #les differents ratios 
    ratio=moyDif/moyIetT
    ratioT=moyDif/moyT
    ratioI=moyDif/moyI
    
    
    flux.write("De l'experience:"+ subjects[i]+"\n")
    flux.write("Moyenne des valeurs absolues des différences sur la moyenne de la force normale du pouce:"+"\n"+str(ratioT)+"\n")
    flux.write("Moyenne des valeurs absolues des différences sur la moyenne de la force normale de l'index:"+"\n"+str(ratioI)+"\n")
    flux.write("Moyenne des valeurs absolues des différences sur la moyenne des forces normales du pouce et de l'index:"+"\n"+str(ratio)+"\n")
    flux.write("\t                "+"-------------------------------------------------------------------------------"+"\n")
    
    i=i+1
    RatioSujets.append(ratio)
    compte=(i)/4
    
    if compte.is_integer(): #Calcule la moyenne des moyennes des valeurs absolues des différences sur la moyenne des forces normales du pouce et de l'index  
        RSM=np.mean(RatioSujets)
        RatioMoySujets.append(RSM)
        RatioSujets.clear()
        
flux.write("Au total cela donne comme ratio(Moyenne des moyennes des valeurs absolues des différences sur la moyenne des forces normales du pouce et de l'index) par personne:"+"\n")
for i in range(4):
    flux.write(str(ListeNom[i])+" : "+str(RatioMoySujets[i])+"\n")

flux.close()    






























