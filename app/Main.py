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

def getColumns(conn, table): #A modifier pour avoir les colonnes
    """
    Retourne une liste contenant plusieurs listes, chacune représentant une colonne.
    Elles sont de la forme [attr, row1Val, row2Val ...]
    """
    cur = conn.cursor()
    slct = "SELECT * FROM "+ table
    cur.execute(slct)

    rows = cur.fetchall()
    
    ret = []
    att = getAttr(conn, table)
    i=0
    while (i < len(att)):
        r = []
        r.append(att[i])
        for row in rows:
            r.append(row[i])
        ret.append(r)
        i+=1
    return ret

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

def getAttr(conn, tabName):
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
        for col in getAttr(conn, tabName[2:-3]):
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
    FD2 = ["Films",["Premiere","Directeur"],["Titre"]]
    FD3 = ["Films",["Acteur","Premiere"],["Titre","Directeur"]]
    FD4 = ["Films",["Acteur","Premiere","Minutes"],["Titre","Directeur"]]
    FD5 = ["Films",["Societe"],["Minutes"]]
    FD6 = ["Films",["Minutes"],["Premiere"]]
    FD7 = ["Films",["Societe"],["Premiere"]]
    FD8 = ["Films",["Societe"],["Acteur"]]
    
    database = "PythonSqlite"
    allTables = []
    allTablesName = ["Films"]
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
            addFuncDep(FD2, allFDs)
            addFuncDep(FD3, allFDs)
            addFuncDep(FD4, allFDs)
            addFuncDep(FD5, allFDs)
            addFuncDep(FD6, allFDs)
            addFuncDep(FD7, allFDs)
            addFuncDep(FD8, allFDs)
            
            # getAllPossibleKeys(getAttr(conn, "tableFilms"))
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
                            print("1. Voir les DFs des tables\n"\
                                "2. Ajouter une DF\n"\
                                "3. Supprimer une DF\n"\
                                "4. Retourner au menu\n")
                            inp = input("")
                            if (inp.isnumeric()):
                                choix = int(inp)
                            else:
                                print("\nChoix non reconnu !")
                        
                        if (choix == 1):                        #Voir les dfs des tables
                            print("Voici les DF des tables: ")
                            for tab in allTablesName:
                                print("  ", tab, ": ")
                                for FD in getFD(allFDs, tab):
                                    print("     ", end="")
                                    printFD(FD)
                        elif (choix == 2):                      #ajouter une df (et proposer dedans des bons candidats)
                            notOk = True
                            _funcDep = []
                            while (notOk):
                                notOk = False
                                print("Voici les DFs conseillées actuellement:")
                                #afficher les DFs conseillées
                                tableName = ""
                                while (tableName not in allTablesName):
                                    tableName = input("Saisissez le nom de la table à laquelle ajouter la DF:")
                                again = True
                                nec = []
                                while (again):
                                    inp = input("Entrez un attribut de la précondition de la DF : ")
                                    if (inp in getAttr(conn, "table"+tableName)):
                                        nec.append(inp)
                                    else:
                                        print(inp, " n'appartient pas aux attributs de la table.")
                                    inp = input("Encore un autre ? (O/N) ")
                                    if (inp == "N" or inp == "0" or inp == "non" or inp == "n"):
                                        again = False
                                again = True
                                csq = []
                                while (again):
                                    inp = input("Entrez un attribut étant déterminé par ceux-ci : ")
                                    if (inp in getAttr(conn, "table"+tableName)):
                                        csq.append(inp)
                                    else:
                                        print(inp, " n'appartient pas aux attributs de la table.")
                                    inp = input("Encore un autre ? (O/N) ")
                                    if (inp == "N" or inp == "0" or inp == "non" or inp == "n"):
                                        again = False
                                _funcDep = [tableName,nec,csq]
                                print(_funcDep, end="")
                                inp = input(" est la DF crée, confirmer ?")
                                if (inp == "N" or inp == "0" or inp == "non" or inp == "n"):
                                    inp = input("Voulez-vous en en recréer une ?")
                                    if (not (inp == "N" or inp == "0" or inp == "non" or inp == "n")):
                                        notOk = True
                            addFuncDep(_funcDep, allFDs)
                            
                        elif (choix == 3):                      #Enlever une df (et proposer dedans des conséquences logiques, non satisfaites ou pas attributs) empêcher les df ou table n'existe pas ?
                            print("Voici toutes les DF actuelles :")
                            i=0
                            while (i<len(allFDs)):
                                print("    ", i, ". ", end="")
                                printFD(allFDs[i])
                                i+=1
                            print("Voici les DFs conseillées:")
                            problematicDFs = getProblematicFDs(conn, allFDs)
                            for FD in problematicDFs:
                                print("     (",FD[1],")     ", allFDs.index(FD[0]), ". ", end="")
                                printFD(FD[0])
                            inp = input("Entrez le numéro de la DF à enlever : ")
                            if (inp.isnumeric() and int(inp)<len(allFDs)):
                                choix = int(inp)
                                removeFuncDep(allFDs[choix], allFDs)
                            else:
                                print("\nChoix non reconnu !")                        
                        elif (choix == 4):                      #Quitter le menu modifiant les DF
                            goOn = False
                        
                        if (goOn):
                            print("\nSouhaitez-vous faire une autre action sur les DFs ?(O/N)\n")
                            inp = input("")
                            if (inp == "N" or inp == "n"):
                                goOn = False
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
                elif (choix == 2): #Voir les clés des tables
                    print("Voici les clés des tables: ")
                    for tab in allTablesName:
                        print("  ", tab, ": ")
                        for key in findKeys(allFDs, tab, getAttr(conn, "table"+tab)):
                            print("     ", key)
                        
                    print("\nAppuyez sur Enter pour continuer.")
                    input("")
                    choix = 0
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
                elif (choix == 3): #Voir quelles tables respectent les normes BCNF et 3NF
                    print("Voici les tables et leurs indications : ")
                    for tab in allTablesName:
                        print("  ", tab, ": ")
                        indications = isTableinBCNFor3NF(tab, allFDs, getAttr(conn, "table"+tab), findKeys(allFDs, tab, getAttr(conn, "table"+tab)))
                        print("     3NF : ", end="")
                        if (indications[0]):
                            print("Oui")
                        else:
                            print("Non à cause des DF suivantes : ")
                            for FD in indications[2]:
                                print("         ", end="")
                                printFD(FD)
                        print("     BCNF : ", end="")
                        if (indications[1]):
                            print("Oui")
                        else:
                            print("Non à cause des DF suivantes : ")
                            for FD in indications[3]:
                                print("         ", end="")
                                printFD(FD)
                        
                    print("\nAppuyez sur Enter pour continuer.")
                    input("")
                    choix = 0
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
                elif (choix == 4): #Quittez le programme
                    cur = conn.cursor()
                    cur.execute("DROP table tableFilms")
                    break
                
    else:
        print("Database connection failed.")
