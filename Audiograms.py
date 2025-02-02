’import sys
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy 
import matplotlib.ticker as ticker
import csv

#Produit le premier seuil random  
#input de fonction=peviousThreshold prends une valeur par hasard entre 0 et 90 de multiple 5
def nextRandomValue(previousThreshold): 
    #définit des limits pour les suivantes seuils random avec le min 0 et le max 90 de multiple 5
    diffmax=25
    lowerLimit=max(0, previousThreshold - diffmax)
    upperLimit=min(95, previousThreshold + diffmax)
    nextValue = random.randrange(lowerLimit, upperLimit, 5) 
    #output de fonction=nextValue donne suivante seuil random par rapport les limites et premier seuil
    return nextValue

#Définit premier audiogramme random avec les limites de seuil (nextRandomValue) et les frequences
#input de fonction=VF le vectuer de frquence qu'on va le donner apres dans le command line 
def nouvelAudiogram(VF):
    vectorFrequency=VF
    #produit le premier audigramme avec tous les seuils randoms 
    previous = random.randrange(0, 95, 5)
    audiogram = [] #une vecteur vide qu'on va le remplisse avec des valeurs randoms de seuil pour produire le premier audiogramme 
    audiogram.append(previous) #avec "append" on joint tous les seuils randoms produit pour obtenir l'audigrame
    #trouve les seuils randoms avec le fonction de "nextrandomvalue" pour toutes les frequences "VF"
    for cpt in range(len(VF)-1):
        nextValue = nextRandomValue(previous)
        audiogram.append(nextValue)
        previous = nextValue
    #output de fonction=audiogram donne le premier audigramme avec ses parametres de seuil et frequence   
    return(audiogram)
   
#définit la difference entre le premier audiogramme random et le deuixieme
#input de fonction= les 2 audiogrammes 
def differenceEntreDeuxAudiogrammes(audio1, audio2):
    scoreDif = 0 #minimum difference entre 2  audiogrammes peut etre 0
    #On calcule un score de différence basé sur la corrélation
    matrice = ((numpy.corrcoef(audio1, audio2)*(-1)) + 1) * 50 
    #on transforme les coefficients de correlations (1 0 -1) a (0 50 100)
    scoreDif = matrice[0,1] #prends les valeurs de diagnal de matrice coef correlations transformes 
    #output de fonction=valeur de correlations entre 2 audigrammes 
    return(scoreDif)



#Crée un nouvel audiogramme très différent des audiogrammes présents dans dfAudiogrammes
#input de fonction=Pour cela, il génère nbAudiogrammesRandom audiogrammes random avec differents frequences et retourne l'audiogramme le plus différent de tous les audiogrammes présents dans dfAudiogrammes 
def creerAudiogrammeDifferent (dfAudiogrammes, nbAudiogrammesRandomToUse, VF):
    # Créer une dataframe temporaire pour mettre les audiogrammes random
    dfAudiogrammesTemp=pd.DataFrame() 
    # Crée nbAudiogrammesRandom audiogrammes random et les insère dans la df temporaire
    # Trouver nbRandomAudiograms audiogrammes random
    for i in range(nbAudiogrammesRandomToUse):
        # on crée un audiogramme random
        audioRandom=nouvelAudiogram(VF)
        # Using DataFrame.insert() to add a column 
        dfAudiogrammesTemp.insert(i, str(i), audioRandom, True) 
    # Pour chacun des audiogrammes random, calcul de la différence moyenne avec tous les audiogrammes présents dans dfAudiogrammes
    dfDifferences  = pd.DataFrame()
    
    # On calcule les differences entre chaque audiogramme random et chaque audiogramme de dfFinale
    for i in list (dfAudiogrammesTemp):
        for j in list (dfAudiogrammes):
            difference = differenceEntreDeuxAudiogrammes(dfAudiogrammesTemp.loc[:,i], dfAudiogrammes.loc[:,j])
            dfDifferences.loc[i,j] = difference
            
    # On ajoute les moyennes
    dfDifferences['mean'] = dfDifferences.mean(axis=1)

    # Trouver l'audiogramme random le plus différent de tous les audiogrammes présents dans dfAudiogrammes
    audiogramme = dfAudiogrammesTemp[dfDifferences['mean'].idxmax()]
    #output de fonction=Retourner cet audiogramme
    return audiogramme
      
#BOUCLE GENERALE
#on cree une autre fonction pour definir les audiograms final et les tracer
def create_audiograms(nbrAudiogramsWanted,nbrAudiogramsbeUsed,VF):
    # On définit le nombre d'audiogrammes très différents qu'on veut
    nbRandomAudiogramsWeWant = nbrAudiogramsWanted
    # On définit le nombre d'audiogrammes random à utiliser pour trouver chaque audiogramme très différent
    nbRandomAudiogramsToUse = nbrAudiogramsbeUsed
    # On crée la base dfFinale avec un premier audiogramme random
    # Génération du premier audiogramme
    #dfs=pd.DataFrame()
    dfFinale=pd.DataFrame(nouvelAudiogram(VF))
    #joint les audiogrammes tres differents l'un et l'autre et les mettre dans le dfFinale l'un apres l'autre
    #df
    #tmp = pd.DataFrame()
    for i in range (nbRandomAudiogramsWeWant):
        audiogrammeNouveau = creerAudiogrammeDifferent(dfFinale,nbRandomAudiogramsToUse, VF)
        dfFinale.append(audiogrammeNouveau)
        dfFinale.insert(i + 1, str(i + 1), audiogrammeNouveau, True)
        print("audiogramme " + str(i+1))
        #for j in list(dfFinale):
            #dfFinale.insert(j + 1, str(j + 1), dfFinale, True)       
    #tracer le plot de dfFinale
    #plt.xlabel('Frequency (kHz)') #définition de l'étiquette de l'axe x
    #plt.ylabel('Threshold (db HL)') #définition de l'étiquette de l'axe y
    #pos_list = numpy.arange(len(VF)) #renvoie des valeurs régulièrement espacées dans un intervalle donné
    #ax = plt.axes() #definir les axes de plot a tracer
    #ax.xaxis.set_major_locator(ticker.FixedLocator((pos_list)))#changer les axes de plot par pos_list et VF 
    #ax.xaxis.set_major_formatter(ticker.FixedFormatter((VF)))
    #plt.plot(dfFinale)
    #plt.ylim(95,0) #limites d'axe y
    #print(plt.show())
    #dfFinale.index=VF #les index(noms de chaque ligne)
    #sauveagrder les donnees finale en csv
    #print("enregistement les audiogrammes")
        #tmp = tmp.append(dfFinale,ignore_index=True)
        #tmp=pd.concat([dfFinale, tmp], axis=1,ignore_index=True)
        #df5000 = pd.merge(df5000, dfFinale, right_index=True, left_index=True, suffixes=[i-1, i])
        dfFin=dfFinale.T
    dfFinale_save=dfFin.to_csv('df5000.csv', mode='a',header=False) 
       
#la fonction main sert de point d'exécution pour tout programme
def main():
    #sys.argv :La liste des arguments de ligne de commande passés à un script Python
    if len(sys.argv)<=3:
        print("you have to write: %run Audiograms.py x y; x:your first value for number of audiorams wanted and  y:your second value for the number of audiograms have to be used")
        #si on donne moin de 3 arguments il affiche rien mais il donne instruction de comment ecrire en terminal
    else:
        #0=nom de fichier 1=1er parametere 2=2eme parametere 3=3eme parameter 
        num1=int(sys.argv[1]) #le nombre d'audiogrammes très différents qu'on veut
        num2=int(sys.argv[2]) #le nombre d'audiogrammes random à utiliser pour trouver chaque audiogramme très différent
        vec_frequences = sys.argv[3].split(",") #le vecteur frequence,changer le delimiter de vecteur frequence par virgule 
        #genere les audiogrammes tres differents avec plusieurs valeurs de frequences en terminal
        for i in range(100):
            create_audiograms(num1,num2,vec_frequences)           
    
if (__name__=="__main__") : #Contrôle l'exécution du code
    main()

    