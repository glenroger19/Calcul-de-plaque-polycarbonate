import numpy as np
import sys
import pandas as pd
from math import sqrt


def coef(c, listeratio , listealpha, listebeta): 
    i = 0
    for i in range (len(listeratio)):
        while listeratio[i] <= c :
            i+= 1
        return (listealpha[i-1] , listebeta[i-1])

param = pd.read_csv('data.csv', sep = "\t")
ratio_ba = list(param[param.columns[0]].values)
alpha = list(param[param.columns[1]].values)
betha = list(param[param.columns[2]].values)

#Initialisation 

lancer_calul = 'Y'
lancer_calul = input("Souhaitez-vous lancer un calcul de dimensionnement de plaque ? \nY or N")
lancer_calul = lancer_calul.upper()

while lancer_calul == 'Y':
    mat = input("Choix du matériau : \n\n - Tapez 'P' pour polycarbonate \n - Tapez 'A' pour autre \n")
    mat = mat.upper()

    if mat == 'P' : 
        physical_characteristic = {'Re' : 83.4, 'E': 2220, 'ν' : 0.38 , 'ratio_ba' : ratio_ba, 'alpha': alpha, 'betha': betha} # dictionnaire
        print ("\nLes caractéristiques physiques du matériaux sont les suivants :  \n\nRe = {} N/mm \nE = {}  Mpa,\nν = {} \n ".format(physical_characteristic['Re'], physical_characteristic['E'],physical_characteristic['ν'] ))
    else :
        print("\nDésolé le matériau n'est pas encore renseigné")
        sys.exit()

    print("\nVeuillez renseigner la largeur a (mm) et la longueur b (mm) de la plaque à étudier")
    answera, answerb = 'N', 'N'
    while answera.upper() != 'Y': 
        a = int(input("\nChoix de la largeur a (mm)"))
        print("\nVous avez choisi une plaque de largeur {} mm".format (a))
        answera = input ("\nConfirmez-vous ce choix ?  \nY or N ")

    while answerb.upper() != 'Y': 
        b = int(input("\nVeuillez renseigner la longueur b (mm) de la plaque à étudier"))
        print("\nVous avez choisi une plaque de longueur {} mm".format (b))
        answerb = input ("\nConfirmez-vous ce choix ?  \nY or N ")

    c = b/a

    coefs = coef(c,physical_characteristic['ratio_ba'], physical_characteristic['alpha'], physical_characteristic['betha'])
    
    # Calcul de la contrainte maximale admissible par la plaque
    safety_coef = 4.5
    sigma_max= physical_characteristic['Re']/safety_coef

    # Calcul de l'épaisseur minimale de la plaque 
    m = 95 # masse des personnes en kg
    g = 9.81 # intensité de la pesanteur à Paris en N/kg
    nmbre_person= 6 # choix du nombre de personnes pour le dimensionnement
    Charge_tot = nmbre_person*m*g
    P_surfacique = Charge_tot/(a*b)
    e = sqrt((6*coefs[1]*P_surfacique*(a**2))/sigma_max)
    print("\nLa valeur de l'épaisseur minimale à choisir est de {} mm pour un coefficient de sécurité fixé à {}". format(int(e)+1,safety_coef) )

    # Calcul de la flèche maximale de la plaque 
    fmax = (coefs[0]*P_surfacique*(a**4))/(physical_characteristic['E']*e**3)
    print ("\nLa flèche maximale correspondante à la plaque d'épaisseur {} mm est de {} mm ". format(int(e)+1, fmax))

    lancer_calul = input("Souhaitez-vous relancer un calcul de dimensionnement de plaque ? \nY or N")



