import sqlite3


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

def readFuncDep(_funcDep):
    notImplemented = True

def addFuncDep(_funcDep, listOfFuncDep):
    notImplemented = True

def removeFuncDep(_funcDep, listOfFuncDep):
    notImplemented = True

def changeFuncDep(_funcDep, listOfFuncDep):
    notImplemented = True

def showFDs(listOfFuncDep):
    notImplemented = True
    
def getProblematicFDs(listOfFuncDep):
    notImplemented = True

def searchNextLogicalConsequence(listOfFuncDep):
    notImplemented = True
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def findKeys(listOfFuncDep, table):             #retourne la liste des clés de la table sur base des FDs
    FDsOnTable = getFD(listOfFuncDep, table)
    notImplemented = True

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
    
