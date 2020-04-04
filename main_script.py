# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:21:28 2020

petit fichier hyper simple pour faire les plots 

Mode d'emploi:
    
    - téléchargez tt les fichiers .glm et .txt du drive
    
    - créez un folder 'masses' et mettez y tt les fichiers .txt avec les masses,
      puis renomez les alex, florent, victor et walid (sans majuscules)
      
    - supprimez l'espace qu'il y a comme premier caractère du fichier masses d'alexandre  
    
    - mettez tt les fichiers .glm ds un fichier 'mesures' (sauf les fichiers des coeffs de friction)
    
    - supprimez le premier fichier d'alex qui n'est pas bon (alex_haut_sans_001) et renomez
      les autres pour que ça aille bien de 1 à 3 et pas de 2 à 4
      
    - créez un folder 'Add' ds le folder 'fichiers'  
      
    - ce fichier est là pour pouvoir utiliser les fonctions hyper facilement
      mais si vous voulez lire les fonctions feel free to amuse yourself :) 
    
@author: Dany
"""
import gbio_example_script_collisions_dany as gbio
 
# il faut modifier ces variables pour dire quoi faire (add prévaut sur Delai qui prévaut sur zoom)

# mettre que les sujets dont on veut les plots
names = ['victor','walid','alex','florent'] # put the subjects' names in here

# mettre True pour faire les moyennes sur les masses et superposer les courbes
Add = False

# mettre True pour calculer les décalages moyen entre grip force avec et grip force sans  
delai = True

# mettre True pour zoomer sur un choc en particulier
zoom = False 
chock = 'alex_haut_sans_001', 1 # choc sur lequel zoomer: bloc, choc    

# a changer que si on veut plot les graphes de base pour un bloc en particulier 
# dans ce cas, il ne faut pas oublier de mettre False pour add, Delai et zoom   

bloc = 'all' # sinon: bloc = 'alex_haut_sans' et trial = 1 correspond au fichier alex_haut_sans_001  
trial = 0    # 0 est la valeur par defaut

# ça sert à rien de toucher à ça, 
# c'est juste pour initialiser les variables 

start = 0
end = 0

#%% pour avoir les plots superposes ou calculer le decalage

if Add or Delai: 
    for name in names:
        if name == 'alex':
            start = 0
            end = 4
        elif name == 'florent': 
            start = 4
            end = 8 
        elif name == 'victor': 
            start = 8
            end = 12
        elif name == 'walid': 
            start = 12
            end = 16
        else:
            print("qu'es-ce que c'est encore que cette histoire ???")
        
        gbio.make_plots(start,end,Name=name,add=Add,Delai=delai) 
    
#%% pour zoomer sur un choc 

elif zoom:  
    name, haut_bas, avec_sans, trial = chock[0].split('_') 
    trial = int(trial[-1])
    
    if name == 'alex':
        start = 0 
    elif name == 'florent': 
        start = 4 
    elif name == 'victor': 
        start = 8 
    elif name == 'walid': 
        start = 12 
            
    if haut_bas == 'haut':
        start += 2 
        
    if avec_sans == 'sans': 
        start += 1
        
    gbio.make_plots(start,start+1,1,zoom=True,chock_number=chock[1],Trial=trial)    
    
#%% pour faire les plots de base

else:    
    if bloc == 'all' and trial == 0:
        gbio.make_plots(0,16) 
    else:
        name, haut_bas, avec_sans = bloc.split('_') 
        
        if name == 'alex':
            start = 0 
        elif name == 'florent': 
            start = 4 
        elif name == 'victor': 
            start = 8 
        elif name == 'walid': 
            start = 12 
            
        if haut_bas == 'haut':
            start += 2 
            
        if avec_sans == 'sans': 
            start += 1
        
        gbio.make_plots(start,start+1,1,Trial=trial) 