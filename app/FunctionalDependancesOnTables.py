import sqlite3
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

def changeFuncDep(_funcDep, listOfFuncDep):
    notImplemented = True
    
def getProblematicFDs(listOfFuncDep):
    notImplemented = True

def searchNextLogicalConsequence(listOfFuncDep):
    notImplemented = True
    
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
    
def findKeys(_listOfFuncDep, _table, _columns):             #retourne la liste des clés de la table sur base des FDs
    FDsOnTable = getFD(_listOfFuncDep, _table)
    allKeys = getAllPossibleKeys(_columns)
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
        for c in _columns:              #Vérifie si keyPoss est bien une clé i.e. elle "implique" toutes les colonnes de la table
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
def BCNFfromDF():
    listOfProblematic = []
    return listOfProblematic
    
def is3NFfromDF():
    listOfProblematic = []
    return listOfProblematic
    
def isTableAndDFinBCNFand3NF():
    #vérifier BCNF
    #si oui vérifier 3NF, si non pas 3NF
    notImplemented = True
    
def whyTableAndDFnotInBCNFand3NF():
    notImplemented = True
    
def exportDecomposition3NF():
    notImplemented = True
    
