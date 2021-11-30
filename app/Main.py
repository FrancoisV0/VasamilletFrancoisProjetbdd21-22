import sqlite3
#a t on besoin d'un vrai funcDep pour chaque table ?
""" A DF will be represented as [string, string[], string[]] """

if __name__=='__main__':
    """needed: a list for all the DF and a list for all the tables"""
    tableExample = "EMP"
    allDFs = []
    
    #allDFs.append() #ajouter un df
    
    print("Bienvenue dans le programme d'essai du module concernant les dépendances fonctionelles sur des tables.\n")
    while(True):
        print("Voici les tables et dépendances fonctionelles sur lesquelles on travaille actuellement:")
        #Afficher les tables une à une avec leurs dfs

        choix = 0
        while (choix not in [1,2,3,4,5]):
            print("Que souhaitez-vous faire ?\n")
            print("1. Voir/modifier une/des DF(s)\n"\
                "2. Enlever/ajouter une/des table(s)\n"\
                "3. Voir les clés des tables\n"\
                "4. Voir quelles tables respectent les normes BCNF et 3NF\n"\
                "5. Quittez le programme\n")
            inp = input("")
            if (inp.isnumeric()):
                choix = int(inp)
            
        goOn = True
        if (choix == 1):   #Voir/modifier une/des DF(s)
            while (goOn):
                choix = 0
                while (choix not in [1,2,3,4]):
                    print("Que souhaitez-vous faire ?\n")
                    print("1. Voir les DFs d'une table\n"\
                        "2. Ajouter une DF\n"\
                        "3. Supprimer une DF\n"\
                        "4. Ne rien faire\n")
                    inp = input("")
                    if (inp.isnumeric()):
                        choix = int(inp)
                #sélectionner une table pour voir ses dfs
                #ajouter une df (et proposer dedans des bons candidats)
                #enlever une df (et proposer dedans des conséquences logiques, non satisfaites ou pas attributs) empêcher les df ou table n'existe pas ?
                #Ne rien faire
                
                if (goOn):
                    print("Souhaitez-vous faire une autre action sur les DFs ?(O/N)\n")
                    inp = input("")
                    if (inp == "N" or inp == "n"):
                        goOn = False
            
        elif (choix == 2): #Enlever/ajouter une/des table(s)
            while (goOn):
                choix = 0
                while (choix not in [1,2,3]):
                    print("Que souhaitez-vous faire ?\n")
                    print("1. Enlever une table\n"\
                        "2. Ajouter une table\n"\
                        "3. Ne rien faire\n")
                    inp = input("")
                    if (inp.isnumeric()):
                        choix = int(inp)
                #Ajouter/enlever une table
                #Ne rien faire
                
                if (goOn):
                    print("Souhaitez-vous faire une autre action sur les tables ?(O/N)\n")
                    inp = input("")
                    if (inp == "N" or inp == "n"):
                        goOn = False
            
        elif (choix == 3): #Voir les clés des tables
            #attendre une confirmation de l'utilisateur avant d'enlever
            choix = 0
            
        elif (choix == 4): #Voir quelles tables respectent les normes BCNF et 3NF
            #marquer ligne par ligne "table  BCNF: ____ 3NF: ____" et en dessous de ladite ligne les raisons si c'est faux
            choix = 0
            while (choix not in [1,2]):
                print("Que souhaitez-vous faire ?\n")
                print("1. Voir la décomposition d'une table\n"\
                    "2. Ne rien faire\n") #reproposer de continuer après
                inp = input("")
                if (inp.isnumeric()):
                    choix = int(inp)
            
            #proposer la décomposition si pas en 3NF
            #Ne rien faire
            #laisser un temps à l'écran
            choix = 0
            
        elif (choix == 5): #Quittez le programme
            exit()
        
    
