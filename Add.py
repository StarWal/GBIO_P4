# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:59:09 2020

@author: Dany
"""
import matplotlib.pyplot as plt
import numpy as np 

name = None
to_cancel = None
accX = None
GF = None
LF = None
dGF = None

def superpose(Name,To_cancel,donnees_accX,donnees_GF,donnees_LF,donnees_dGF):
    global accX, GF, LF, dGF, name, to_cancel
         
    name = Name  
    to_cancel = To_cancel 
    accX = donnees_accX
    GF = donnees_GF
    LF = donnees_LF
    dGF = donnees_dGF
    
    fig = plt.figure(figsize = [8,10])
    ax  = fig.subplots(4,2)
    
    fig.suptitle(name, fontsize=16)
    
    ax[0,0].set_title("Haut", fontsize=14)
    ax[0,1].set_title("Bas", fontsize=14)
    
    ax[0,0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
    ax[1,0].set_ylabel("LF [N]", fontsize=13)
    ax[2,0].set_ylabel("GF [N]", fontsize=13)
    ax[3,0].set_ylabel("GF derivative [N/s]", fontsize=13)
    
    ax[3,0].set_xlabel("Time [ms]", fontsize=13)
    ax[3,1].set_xlabel("Time [ms]", fontsize=13)
    
    new_accX,new_GF,new_LF,new_dGF = Sum()
    time = np.arange(0,1200)
     
    colors = ['r','b','r','b']
    cols = [0,0,1,1]
    lines = [None,None,None,None]
    for i in range(4):
        col = cols[i]
        color = colors[i] 
        for item_accX,item_GF,item_LF,item_dGF in zip(new_accX[i],new_GF[i],new_LF[i],new_dGF[i]):
            lines[i] = ax[0,col].plot(time,item_accX,color)
            ax[1,col].plot(time,item_LF,color)
            ax[2,col].plot(time,item_GF,color)
            ax[3,col].plot(time,item_dGF,color)
    lines = (lines[0][0],lines[1][0])  
    fig.legend(lines, ('avec anticipation', 'sans anticipation'), loc='upper right')    
    fig.savefig("figures\Add\%s_acc_forces_dGF.png" %(name)) 
    
def Sum():   
    global accX, GF, LF, dGF, name
    
    new_donnees_accX = [[None,None,None] for i in range(4)] 
    new_donnees_GF = [[None,None,None] for i in range(4)]   
    new_donnees_LF = [[None,None,None] for i in range(4)]   
    new_donnees_dGF = [[None,None,None] for i in range(4)]  
     
    # somme sur chaque masse pour les 3 memes blocs
    ind,blocks_ind,choc_number = block_order() 
    for i in range(12): 
        ind_1,ind_2 = blocks_ind[str(i+1)]
        for j in range(3):
            for k in ind[str(i+1)][str(j+1)]:
                if type(k) == int:
                    k = [k]
                for l in k:
                    L = 0 
                    for item_accX,item_GF,item_LF,item_dGF in zip(accX[ind_1][ind_2],GF[ind_1][ind_2],LF[ind_1][ind_2],dGF[ind_1][ind_2]):
                        if l == L: 
                            if np.all(new_donnees_accX[ind_1][j]) == None:
                                new_donnees_accX[ind_1][j] = item_accX
                                new_donnees_GF[ind_1][j] = item_GF
                                new_donnees_LF[ind_1][j] = item_LF 
                                new_donnees_dGF[ind_1][j] = item_dGF
                            else:
                                new_donnees_accX[ind_1][j] += item_accX
                                new_donnees_GF[ind_1][j] += item_GF
                                new_donnees_LF[ind_1][j] += item_LF 
                                new_donnees_dGF[ind_1][j] += item_dGF
                        L += 1        
    
    # termine le calcul de la moyenne en divisant par le nombre de chocs correspondant
    for i in range(4):
        for j in range(3): 
            new_donnees_accX[i][j] = new_donnees_accX[i][j] / choc_number[i][j]
            new_donnees_GF[i][j] = new_donnees_GF[i][j] / choc_number[i][j]
            new_donnees_LF[i][j] = new_donnees_LF[i][j] / choc_number[i][j]
            new_donnees_dGF[i][j] = new_donnees_dGF[i][j] / choc_number[i][j]
                    
    return new_donnees_accX, new_donnees_GF, new_donnees_LF, new_donnees_dGF                        
                    
def block_order():
    global name, to_cancel
    try:  
        first = 0 ; Next = 0
        if name == 'alex':
            first = 1
            Next = 0 
        elif name == 'walid':
            first = 3
            Next = 2 
        elif name == 'victor': # finalement il a commencé avec ou sans anticipation ?
            first = 1
            Next = 0 
        elif name == 'florent':
            first = 2
            Next = 3
        else: 
            print('WTF is going on with your filename ???') 
            
        blocks_ind = {}    
        for i in range(6):
            if i < 3:
                blocks_ind[str((i*2)+1)] = first,i
                blocks_ind[str((i*2)+2)] = Next,i
            else: 
                new_first = 0 ; new_next = 0
                if first < 2:
                    new_first = first+2
                    new_next = Next+2
                else:
                    new_first = first-2
                    new_next = Next-2
                blocks_ind[str((i*2)+1)] = new_first,i-3
                blocks_ind[str((i*2)+2)] = new_next,i-3
        
        filename = 'masses\%s.txt' %(name)
        file = open(filename,'r')
        
        ind = {} ; choc_number = {} ; block = '' ; n = 0
        for num,line in enumerate(file.readlines()):
            if line[:4] == 'Bloc':
                block = line.split(' ')[1][:-1] 
                ind[block] = {'1':[],'2':[],'3':[]}
                choc_number[block] = {'1':0,'2':0,'3':0}
                n = 0    
            elif not line == "\n":
                mass = line.split(' ')[4][0]
                ind[block][mass].append(n)
                choc_number[block][mass] += 1
                n = n+1
        file.close()  
        
        for j in range(6):
            for k in ['1','2','3']:
                if j<3:
                    for l in ind[str((j*2)+1)][k]:
                        if to_cancel[first][j] != []:
                            for h in to_cancel[first][j]:
                                if l == h:
                                    choc_number[str((j*2)+1)][k] -= 1 
                    for l in ind[str((j*2)+2)][k]:
                        if to_cancel[Next][j] != []:
                            for h in to_cancel[Next][j]:
                                if l == h:
                                    choc_number[str((j*2)+2)][k] -= 1    
                else:
                    new_first = 0 ; new_next = 0
                    if first < 2:
                        new_first = first+2
                        new_next = Next+2
                    else:
                        new_first = first-2
                        new_next = Next-2
                    for l in ind[str((j*2)+1)][k]:  
                        if to_cancel[new_first][j-3] != []:
                            for h in to_cancel[new_first][j-3]:
                                if l == h:
                                    choc_number[str((j*2)+1)][k] -= 1 
                    for l in ind[str((j*2)+2)][k]:
                        if to_cancel[new_next][j-3] != []:
                            for h in to_cancel[new_next][j-3]:
                                if l == h:
                                    choc_number[str((j*2)+2)][k] -= 1  
        
        new_choc_number = [[0,0,0] for i in range(4)]
        for i in range(12):
            k,_ = blocks_ind[str(i+1)] 
            for j in range(3):
                new_choc_number[k][j] += choc_number[str(i+1)][str(j+1)] 
            
        return ind, blocks_ind, new_choc_number      
    except Exception:
        raise
    finally:
        if file != None:
            file.close()