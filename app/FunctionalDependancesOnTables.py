import sqlite3
from Main import *
from itertools import chain, combinations

def getFD(_listOfFDs, _tabName):          #retourne liste des FD de la table _table
    ret = []
    for fd in _listOfFDs:
        if (fd[0] == _tabName):
            ret.append(fd)
    return ret

def printFD(_FD):
    for i in range(len(_FD[1])):
        if (i!=0):
            print(", ",end="")
        print(_FD[1][i],end="")
    print("  -->  ",end="")
    for i in range(len(_FD[2])):
        if (i!=0):
            print(", ",end="")
        print(_FD[2][i],end="")
    print("")

def getNec(FD):
    nec = []
    for c in FD[1]:
        nec.append(c)
    return nec
    
def getCsq(FD):
    csq = []
    for c in FD[2]:
        csq.append(c)
    return csq

def addFuncDep(tableName, columns1, columns2, listOfFuncDep):
    listOfFuncDep.append([tableName,columns1,columns2])

def addFuncDep(_FD, listOfFuncDep):
    listOfFuncDep.append(_FD)

def removeFuncDep(_FD, listOfFuncDep):
    for i in range(len(listOfFuncDep)):
        fd = listOfFuncDep[i]
        same = True
        if (fd[0] == _FD[0]):
            for c in fd[1]:
                if (c not in _FD[1]):
                    same = False
            for c in _FD[1]:
                if (c not in fd[1]):
                    same = False
            for c in fd[2]:
                if (c not in _FD[2]):
                    same = False        
            for c in _FD[2]:
                if (c not in fd[2]):
                    same = False
        else:
            same = False
        if (same):
            listOfFuncDep.pop(i)
            return True
    return False

def getAdvicedFD(_listOfFuncDep, _table, _attr):
    ret = []
    cols = getColumns(conn, "table"+FD[0])
    for attr in _attr:
        for col in cols:
            if (col[0] != attr):
                csq = []
                #si il implique un autre attribut, l'ajouter à csq
                #si csq pas vide, l'ajouter à ret
    for col1 in cols:
        for col in cols[cols.index(col1):]:
            csq = []
            #si ils impliquent un autre attribut, l'ajouter à csq
            #si csq pas vide, l'ajjouter à ret
    #enlever toutes les conséquences logiques de la liste (qui sont déjà présent avant)
    
def getProblematicFDs(conn, _listOfFuncDep):
    ret = [] #On retourne une liste de tuple de la forme (df,raisonDeRejet)
    #df redondante
    for DF1 in _listOfFuncDep:
        for DF2 in _listOfFuncDep:
            for DF3 in _listOfFuncDep:
                if(DF1 != DF2 and DF2 != DF3 and DF1 != DF3):
                    nec1, nec2, nec3 = getNec(DF1), getNec(DF2), getNec(DF3)
                    csq1, csq2, csq3 = getCsq(DF1), getCsq(DF2), getCsq(DF3)
                    bool = True
                    for a in nec1:
                        if (a not in nec2):
                            bool = False
                    if (bool and csq1 == csq2):
                        ret.append((DF2,"La DF est redondante"))
                    if (nec1 == nec3 and csq1 == nec2 and csq2 == csq3):
                        ret.append((DF3,"La DF est déjà une conséquence logique"))
    #df pas respectée
    for FD in _listOfFuncDep:
        cols = getColumns(conn, "table"+FD[0])
        n, c = getNec(FD), getCsq(FD)
        nec, csq = [], []
        for col in cols:
            if (col[0] in n):
                nec.append(col)
            elif (col[0] in c):
                csq.append(col)
        i = 1
        while (i < len(nec[0])):
            j = 1
            while (i+j < len(nec[0])):
                bool1 = True
                for n1 in nec:
                    if (n1[i] != n1[j]):
                        bool1 = False
                if (bool1):
                    for c1 in csq:
                        if (c1[i] != c1[j]):
                            ret.append((FD,"La DF n'est pas respectée"))
                j+=1
            i+=1
    for r1 in ret:              #Elimine les doublons de la liste
        i = ret.index(r1) + 1
        while (i < len(ret)):
            if (r1 == ret[i]):
                ret.pop(i)
                i-=1
            i+=1
    return ret
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getAllPossibleKeys(_columns):       #Retourne toutes les clés possibles i.e. une combinaison de toutes les colonnes
    allKeysPoss = []
    s = list(_columns)
    for x in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)):
        if (len(x) != 0):               #La liste nulle ne nous intéresse pas
            if (len(x) == 1):
                x = [str(str(x)[2:-3])]
            else:
                x = list(x)
            allKeysPoss.append(x)
    return allKeysPoss
    
def copyCol(listOfCol):                 #Fait une deepcopy d'une liste de colonnes
    ret = []
    for c in listOfCol:
        ret.append(c)
    return ret
    
def findKeys(_listOfFuncDep, _table, _attr):             #retourne la liste des clés de la table sur base des FDs
    FDsOnTable = getFD(_listOfFuncDep, _table)
    allKeys = getAllPossibleKeys(_attr)
    ret = []
    for keyPoss in allKeys:
        actCol = copyCol(keyPoss)       #Cette liste ajoute les colonnes "impliquée" par la clé au fur et à mesure des dfs
        retry = True
        while (retry):
            retry = False
            for fd in FDsOnTable:
                nec = getNec(fd)
                csq = getCsq(fd)
                for c in actCol:        #On regarde pour chaque colonne si elle est dans les éléments nécessaire de la df, si oui on supprime cette col
                    if (c in nec):
                        nec.remove(c)
                if (not nec):           #Si la liste des éléments nécessaires est vide, on peut dire que toutes les conditions sont respecétes et ajouté les éléments conséquences de la df à notre liste de col
                    for c in csq:
                        if (c not in actCol):
                            actCol.append(c)
                            retry = True
        cont = True
        for c in _attr:              #Vérifie si keyPoss est bien une clé i.e. elle "implique" toutes les colonnes de la table
            if (c not in actCol):
                cont = False
        if (cont):
            ret.append(keyPoss)
    for key1 in ret:                    #On supprime les clés redondates (toute clé plus grande que key1 et qui contient key1)
        for key2 in ret[ret.index(key1):]:
            if (len(key1) < len(key2)):
                keyTmp = copyCol(key1)
                for c in key1:
                    if (c in key2):
                        keyTmp.remove(c)
                if (not keyTmp):
                    ret.remove(key2)
    return ret
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def isTableinBCNFor3NF(_table, _listOfFuncDep, _attr, _tableKeys):
    boolBCNF = True
    reasonNotBCNF = []
    bool3NF = True
    reasonNot3NF = []
    FDsOnTable = getFD(_listOfFuncDep, _table)
    for FD in FDsOnTable:
        nec = getNec(FD)
        csq = getCsq(FD)
        if (nec not in _tableKeys):
            boolBCNF = False
            reasonNotBCNF.append(FD)
            csqInKey = False
            for Key in _tableKeys:
                if (csq in Key):
                    csqInKey = True
            if (not csqInKey):
                bool3NF = False
                reasonNot3NF.append(FD)
    return [bool3NF,boolBCNF,reasonNot3NF,reasonNotBCNF]