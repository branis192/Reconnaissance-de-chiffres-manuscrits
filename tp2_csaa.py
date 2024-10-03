# -*- coding: utf-8 -*-
"""TP2_CSAA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y7If5cSuYVg1RE5o1es9_Q_EX5tsdm9a

# TP2 - Reconnaissance de chiffres manuscrits par $k$ plus proches voisins

L'objectif de ce TP est de reconnaître des chiffres manuscrits d'une base de test à partir d'une base d'apprentissage et de la méthode des $k$ plus proches voisins.
La base de données du MNIST{\footnote{http://yann.lecun.com/exdb/mnist/}} sur les chiffres manuscrits comprend un ensemble de 60 000 exemples d'apprentissage (*database_train_images*) et un ensemble de 10 000 exemples de test (*database_test_images*).  Les chiffres, dont quelques exemples sont représentés sur la figure ci-dessous, ont été normalisés et centrés dans une image de taille fixe $28\times 28$ pixels.

<img src="files/MNIST.PNG" width="600" height="400"  >




Chaque image est considérée comme un vecteur 1D de $28\times 28=784$ coordonnées. On fournit les labels des ensembles d'apprentissage (*y_train*) et de test
(*y_test*).
"""

import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import math
import scipy as sc
from sklearn.metrics.pairwise import euclidean_distances

"""### Chargement de la base de données MNIST

Lien du dataset des chiffres manuscrits :
http://yann.lecun.com/exdb/mnist/
"""

from sklearn.datasets import fetch_openml
mnist = fetch_openml("mnist_784")

X, y = mnist["data"], mnist["target"]

DataApp , DataTest , LabelApp , LabelTest = X[:60000] , X[60000:] , y[:60000] , y[60000:]

print('DataApp: ' + str(DataApp.shape))
print('DataTest:' + str(DataTest.shape))
print(' LabelApp:  '  + str(LabelApp.shape))
print('LabelTest:  '  + str(LabelTest.shape))

# Conversion en matrices
DataApp=np.asarray(DataApp)
DataTest=np.asarray(DataTest)
LabelApp=np.asarray(LabelApp)
LabelTest=np.asarray(LabelTest)

# Affichage d'images de ce jeu de données :

# on affiche une donnée image de X_train et X_test :
NumImageTrain=12345 # à choisir entre 0 et 59999
Exple1=DataApp[NumImageTrain,:]
ImExple1=np.reshape(Exple1,[28,28])
plt.imshow(ImExple1)
plt.show()
print("le label de cette image d'apprentissage est :", LabelApp[NumImageTrain])

NumImageTest=1234 # à choisir entre 0 et 9999
Exple2=DataTest[NumImageTest,:]
ImExple2=np.reshape(Exple2,[28,28])
plt.imshow(ImExple2)
plt.show()
print("le label de cette image de test est :", LabelTest[NumImageTest])



"""## Exercice 1 : méthode des $k$ plus proches voisins

En intelligence artificielle, la méthode des $k$ plus proches voisins  ($k$-ppv) est une méthode d'apprentissage supervisé.
Dans ce cadre, on dispose d'une base de données d'apprentissage constituée de couples « donnée-label ». Pour estimer la sortie associée à une nouvelle entrée $x$, la méthode des $k$ plus proches voisins consiste à prendre en compte (de façon identique) les $k$ échantillons d'apprentissage dont l'entrée est la plus proche de la nouvelle entrée $x$, selon une distance à définir. L'algorithme  associé  et un exemple sont donnés par la suite.



<img src="files/AlgoKppv.png" width="900" height="800"  >

<img src="files/kppv.png" width="300" height="300"  >


**Exemple de classification $k$-ppv:** L'échantillon de test (cercle vert) doit être classé soit dans la première classe des carrés bleus, soit dans la deuxième classe des triangles rouges. Si k = 3 (cercle plein), il est assigné à la deuxième classe parce qu'il y a 2 triangles et seulement 1 carré à l'intérieur du cercle intérieur. Si k = 5 (cercle en pointillés), il est assigné à la première classe (3 carrés contre 2 triangles à l'intérieur du cercle extérieur)

**Question :**
En utilisant la distance euclidienne, complétez la fonction *kppv* permettant d'effectuer la classification par $k$-ppv sur un ensemble de test à partir d'un ensemble d'apprentissage et de leurs labels et en spécifiant le nombre $k$  voisins que l'on cherche.

### Fonctions python intéressantes :
Liste de fonctions (librairies) :

- euclidean_distances (sklearn)
- mode (scipy.stats) [à changer pour traiter le cas d'égalité]
- argsort (numpy)
- argmax (numpy)
- unique (numpy)
"""

def kppv(DataApp,DataTest,labelApp,K,Nt_test):

    Na=DataApp.shape[0]
    Nt=DataTest.shape[0]


    # Initialisation du vecteur d'etiquetage des images tests
    Partition = np.zeros((Nt_test,1));

    # Boucle sur les vecteurs test de l'ensemble de l'evaluation
    for i in range(Nt_test):

        print('Image test n',i)

        # Calcul des distances entre les vecteurs de test
        # et les vecteurs d'apprentissage (voisins)

        distance = euclidean_distances(DataTest[i].reshape((1,-1)),DataApp)

        # # On ne garde que les indices des K + proches voisins

        kpp = np.argsort(distance[0])[:K]

        # # Comptage du nombre de voisins appartenant a chaque classe

        labelpp = labelApp[kpp]


        # # Recherche de la classe contenant le maximum de voisins

        (values, counts) = np.unique(labelpp, return_counts=True)
        print(counts)
        maxindex = np.argmax(counts)
        print(maxindex)
        class_max = values[maxindex]

        # # Si l'image test a le plus grand nombre de voisins dans plusieurs
        # # classes differentes, alors on lui assigne celle du voisin le + proche,
        # # sinon on lui assigne l'unique classe contenant le plus de voisins

        # print(class_max)

        if np.sum(counts == counts[maxindex]) > 1:
            Partition[i] = labelpp[0]
        else:
            Partition[i] = class_max


        # Assignation de l'etiquette correspondant ‡ la classe trouvee au point
        # correspondant a la i-eme image test dans le vecteur "Partition"

        print('Partition ', i , ' = ' ,Partition[i])


    return Partition

# Choix du nombre de voisins
K = 1;

# Nombre de données à tester
Nt=DataTest.shape[0]
Nt_test = int(Nt/1000); # A changer, pouvant aller jusqu'a Nt


# Classement par aux k-ppv
Partition = kppv(DataApp,DataTest,LabelApp,K,Nt_test);

# Affichage des résultats de prédiction et de vérité terrainMatriceConfusion=np.zeros((10,10))
print('Resultat Kppv',Partition.T)
print('Vérité terrain',LabelTest[:Nt_test])

"""## Exercice 2 : évaluation de la reconnaissance

En disposant des labels exacts des données de l'ensemble de test, l'évaluation de la bonne reconnaissance est réalisée par une matrice de confusion et par un taux d'erreur:
- La matrice de confusion est une matrice $10\times 10$ dont l'élément générique d'indice $(i,j)$ est le nombre de vecteurs de classe correspondant à l'indice $i$ qui ont été affectés à la classe correspondant à l'indice $j$ par le processus de décision. Si la matrice de confusion est diagonale alors la reconnaissance est parfaite.
- le taux d'erreur correspond à un pourcentage défini par le nombre d'éléments hors diagonaux de la matrice de confusion divisé par le nombre total d'éléments testés.

<img src="files/MatConfus.PNG" width="600" height="400"  >

**Question :**
- En utilisant les labels de l'ensemble de test, complétez *kppv* afin de rajouter le calcul de la matrice de confusion et le taux d'erreur.
- Testez l'algorithme pour $k=1$ et $k=10$ et calculez les taux d'erreur respectifs.
"""

