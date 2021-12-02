import sqlite3
from sqlite3 import Error
from FunctionalDependancesOnTables import *
#a t on besoin d'un vrai funcDep pour chaque table ?
""" A DF will be represented as [string, string[], string[]] """

#Tables utilisées pour ce fichier



def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return conn
    
def create_table(conn, createTableSql):
    try:
        c = conn.cursor()
        c.execute(createTableSql)
    except Error as e:
        print(e)
    
def printTable(_table):     #affiche à l'écran la table de façon correcte
    notImplemented = True


if __name__=='__main__':
    """needed: a list for all the DF and a list for all the tables"""
    database = "PythonSqlite"
    allTablesName = []
    
    table1 = """CREATE TABLE IF NOT EXISTS table1(
        qqc1 text PRIMARY KEY,
        qqc2 text NOT NULL,
        qqc3 integer,
        FOREIGN KEY (qqc3) REFERENCES table2 (qqch21)
    );"""
    
    allTablesName.append(table1)
    
    conn = create_connection(database)
    if conn is not None:
        create_table(conn,table1)
        allFDs = []
        
        
        #allFDs.append() #ajouter un df
        
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        print("\nBienvenue dans le programme d'essai du module concernant les dépendances fonctionelles sur des tables.")
        while(True):
            print("Voici les tables et dépendances fonctionelles sur lesquelles on travaille actuellement:")
            #Afficher les tables une à une avec leurs dfs

            choix = 0
            while (choix not in [1,2,3,4,5]):
                print("\nQue souhaitez-vous faire ?\n")
                print("1. Voir/modifier une/des DF(s)\n"\
                    "2. Enlever/ajouter une/des table(s)\n"\
                    "3. Voir les clés des tables\n"\
                    "4. Voir quelles tables respectent les normes BCNF et 3NF\n"\
                    "5. Quittez le programme\n")
                inp = input("")
                if (inp.isnumeric()):
                    choix = int(inp)
                else:
                    print("\nChoix non reconnu !")
                
            goOn = True
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if (choix == 1):   #Voir/modifier une/des DF(s)
                while (goOn):
                    choix = 0
                    while (choix not in [1,2,3,4]):
                        print("Que souhaitez-vous faire ?\n")
                        print("1. Voir les DFs d'une table\n"\
                            "2. Ajouter une DF\n"\
                            "3. Supprimer une DF\n"\
                            "4. Retourner au menu\n")
                        inp = input("")
                        if (inp.isnumeric()):
                            choix = int(inp)
                        else:
                            print("\nChoix non reconnu !")
                    
                    if (choix == 1):#sélectionner une table pour voir ses dfs
                        #choisir une table
                        showFDs(getFD(allFDs, tab))
                        
                    elif (choix == 2):#ajouter une df (et proposer dedans des bons candidats)
                        print("Voici les DFs conseillées actuellement:")
                        #afficher les DFs conseillées
                        tableName = ""
                        while (tableName not in allTablesName):
                            tableName = input("Saisissez le nom de la table à laquelle ajouter la DF:")
                        #prendre aussi les colonnes qui définissent la DF
                        _funcDep = []
-                        addFuncDep(_funcDep, allFDs)
                        
                    
                    elif (choix == 3):#enlever une df (et proposer dedans des conséquences logiques, non satisfaites ou pas attributs) empêcher les df ou table n'existe pas ?
                        print("Voici les DFs conseillées actuellement:")
                        problematicDFs = getProblematicDFs(allFDs)
                        #afficher les DFs conseillées
                        while (tableName not in allTablesName):
                            tableName = input("Saisissez le nom de la table à laquelle ajouter la DF:")
                        allFDforTab = getFD(allFDs, tableName)
                        #afficher les DFs une à une et sélectionner celle à enlever
                        _funcDep = []
                        removeFuncDep(_funcDep, allFDs)
                    
                    elif (choix == 4):
                        goOn = False
                    
                    if (goOn):
                        print("Souhaitez-vous faire une autre action sur les DFs ?(O/N)\n")
                        inp = input("")
                        if (inp == "N" or inp == "n"):
                            goOn = False
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------            
            elif (choix == 2): #Enlever/ajouter une/des table(s)
                while (goOn):
                    choix = 0
                    while (choix not in [1,2,3]):
                        print("Que souhaitez-vous faire ?\n")
                        print("1. Enlever une table\n"\
                            "2. Ajouter une table\n"\
                            "3. Retourner au menu\n")
                        inp = input("")
                        if (inp.isnumeric()):
                            choix = int(inp)
                        else:
                            print("\nChoix non reconnu !")
                            
                    
                    if (choix == 1):#Ajouter une table
                        notImplemented = True
                        
                    elif (choix == 2):#Enlever une table
                        notImplemented = True
                        
                    elif (choix == 3):#Ne rien faire
                        goOn = False
                    
                    if (goOn):
                        print("Souhaitez-vous faire une autre action sur les tables ?(O/N)\n")
                        inp = input("")
                        if (inp == "N" or inp == "n"):
                            goOn = False
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
            elif (choix == 3): #Voir les clés des tables
            
                for tab in allTables:
                    print(tab)
                    for key in findKeys(allFDforTab, tab):
                        print(key)
                    
                print("Appuyez sur Enter pour continuer.")
                input("")
                choix = 0
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
            elif (choix == 4): #Voir quelles tables respectent les normes BCNF et 3NF
          
                #marquer ligne par ligne "nomTable  BCNF: ____ 3NF: ____" et en dessous de ladite ligne les raisons si c'est faux
                
                while (goOn):
                    choix = 0
                    while (choix not in [1,2]):
                        print("Que souhaitez-vous faire ?\n")
                        print("1. Voir la décomposition d'une table\n"\
                            "2. Retourner au menu\n")
                        inp = input("")
                        if (inp.isnumeric()):
                            choix = int(inp)
                        else:
                            print("\nChoix non reconnu !")
                    
                    
                    if (choix == 1):#Voir la décomposition d'une table
                        notImplemented = True
                    #demander une table et le faire
                    
                    if (choix == 2):
                        goOn=False
                    if (goOn):
                        print("Souhaitez-vous voir la décomposition d'une autre table ?(O/N)\n")
                        inp = input("")
                        if (inp == "N" or inp == "n"):
                            goOn = False
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
            elif (choix == 5): #Quittez le programme
                exit()
            
    else:
        print("Database connection failed.")
