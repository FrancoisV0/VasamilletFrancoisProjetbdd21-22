import sqlite3
import os
from sqlite3 import Error
from FunctionalDependancesOnTables import *
#a t on besoin d'un vrai funcDep pour chaque table ?
""" A DF will be represented as [string, string[], string[]] """

#Tables utilisées pour ce fichier


"""Les X fonctions qui suivent sont reprises directement du tutoriel sqlite3 trouvé sur sqlitetutorial.net/sqlite-python"""
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
    
def create_table(conn, createTableSql):
    try:
        c = conn.cursor()
        c.execute(createTableSql)
    except Error as e:
        print(e)

def createRowInTableFilms(conn, row):
    """
    Create a new row into the tableFilms table
    :param conn:
    :param row:
    :return: tableFilms id
    """
    sql = ''' INSERT INTO tableFilms(Titre,Directeur,Acteur,Societe,Premiere,Minutes)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, row)
    conn.commit()
    return cur.lastrowid
    
def selectAllRowsInTable(conn, table):
    """
    Query all rows in the table table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    slct = "SELECT * FROM "+ table
    cur.execute(slct)

    rows = cur.fetchall()

    for row in rows:
        for c in row:
            print(c, " "*(22-len(str(c))), end = "")
        print("")

def getColumns(conn, tabName):
    ret = []
    tableInfo = "PRAGMA table_info("+tabName+")"
    cur = conn.cursor()
    cur.execute(tableInfo)
    for info in cur.fetchall():
        ret.append(info[1])
    return ret

def printAllTablesAndFD(conn, fds):     #affiche à l'écran les tables de façon correcte
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_schema WHERE type='table'")
    tables = (cur.fetchall())
    for tabName in tables:
        tabName = str(tabName)
        print("'"+tabName[7:-2], "\n")
        for col in getColumns(conn, tabName[2:-3]):
            print(col, " "*(22-len(str(col))), end = "")
        print("")
        selectAllRowsInTable(conn, tabName[2:-3])
        print("")
        fdsForTab = getFD(fds, tabName[7:-3])
        for fd in fdsForTab:
            printFD(fd)
        print("\n")
    
if __name__=='__main__':
    tableFilms = """CREATE TABLE IF NOT EXISTS tableFilms(
        Titre text,
        Directeur text,
        Acteur text,
        Societe text,
        Premiere text,
        Minutes int
    );"""
    row1 = ("The Birds", "A. Hitchcock", "T. Hedren", "Universal Pictures", "28/03/1963", 113)
    row2 = ("The Birds", "A. Hitchcock", "R. Taylor", "Universal Pictures", "28/03/1963", 113)
    row3 = ("Titanic", "J. Cameron", "K. Winslet", "Twentieth Century Fox", "19/12/1997", 195)
    row4 = ("Titanic", "J. Cameron", "L. DiCaprio", "Twentieth Century Fox", "19/12/1997", 195)
    row5 = ("The Birds", "J. Cameron", "K. Winslet", "Paramount Pictures", "28/01/2001", 182)
    row6 = ("The Birds", "J. Cameron", "R. Taylor", "Paramount Pictures", "28/01/2001", 182)
    
    FD1 = ["Films",["Titre","Directeur"],["Societe","Premiere","Minutes"]]
    
    database = "PythonSqlite"
    allTables = []
    allFDs = []
    allRowsTableFilms = []
    
    
    allTables.append(tableFilms)
    allRowsTableFilms.append(row1)
    allRowsTableFilms.append(row2)
    allRowsTableFilms.append(row3)
    allRowsTableFilms.append(row4)
    allRowsTableFilms.append(row5)
    allRowsTableFilms.append(row6)
        
    conn = create_connection(database)
    if conn is not None:
        with conn:
            for tab in allTables:
                create_table(conn,tab)
            for row in allRowsTableFilms:
                createRowInTableFilms(conn, row)
            addFuncDep(FD1, allFDs)
            
            # getAllPossibleKeys(getColumns(conn, "tableFilms"))
            #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            print("\nBienvenue dans le programme d'essai du module concernant les dépendances fonctionelles sur des tables.")
            while(True):
                print("Voici les tables et dépendances fonctionelles sur lesquelles on travaille actuellement:\n")
                printAllTablesAndFD(conn, allFDs)

                choix = 0
                while (choix not in [1,2,3,4]):
                    print("\nQue souhaitez-vous faire ?\n")
                    print("1. Voir/modifier une/des DF(s)\n"\
                        "2. Voir les clés des tables\n"\
                        "3. Voir quelles tables respectent les normes BCNF et 3NF\n"\
                        "4. Quittez le programme\n")
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
                            addFuncDep(_funcDep, allFDs)
                            
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
                elif (choix == 2): #Voir les clés des tables
                
                    for tab in allTables:
                        print(tab)
                        for key in findKeys(allFDforTab, tab):
                            print(key)
                        
                    print("Appuyez sur Enter pour continuer.")
                    input("")
                    choix = 0
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
                elif (choix == 3): #Voir quelles tables respectent les normes BCNF et 3NF
              
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
                elif (choix == 4): #Quittez le programme
                    cur = conn.cursor()
                    cur.execute("DROP table tableFilms")
                    break
                
    else:
        print("Database connection failed.")
