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
def getAllPossibleKeys(_columns):
    allKeysPoss = []
    s = list(_columns)
    for x in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)):
        if (len(x) != 0):
            if (len(x) == 1):
                x = [str(str(x)[2:-3])]
            else:
                x = list(x)
            allKeysPoss.append(x)
    print(allKeysPoss)
    return allKeysPoss

def findKeys(_listOfFuncDep, _table, _columns):             #retourne la liste des clés de la table sur base des FDs
    FDsOnTable = getFD(_listOfFuncDep, _table)
    

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
    
