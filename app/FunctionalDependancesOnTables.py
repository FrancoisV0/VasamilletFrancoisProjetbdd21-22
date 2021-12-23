import sqlite3
from itertools import chain, combinations

def getFD(_listOfAllFD, _tabName):          #retourne la liste des DF de la table _tabName
    ret = []
    for fd in _listOfAllFD:
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

def getNec(_FD):
    nec = []
    for n in _FD[1]:
        nec.append(n)
    return nec
    
def getCsq(_FD):
    csq = []
    for c in _FD[2]:
        csq.append(c)
    return csq

def addFuncDep(_tabName, _nec, _csq, _listOfAllFD):
    listOfFuncDep.append([_tabName,_nec,_csq])

def addFuncDep(_FD, _listOfAllFD):
    _listOfAllFD.append(_FD)

def removeFuncDep(_FD, _listOfAllFD):
    for i in range(len(_listOfAllFD)):
        FD = _listOfAllFD[i]
        same = True
        if (FD[0] == _FD[0]):
            for c in FD[1]:
                if (c not in _FD[1]):
                    same = False
            for c in _FD[1]:
                if (c not in FD[1]):
                    same = False
            for c in FD[2]:
                if (c not in _FD[2]):
                    same = False        
            for c in _FD[2]:
                if (c not in FD[2]):
                    same = False
        else:
            same = False
        if (same):
            listOfFuncDep.pop(i)
            return True
    return False

def getAdvicedFD(_columns, _tabName, _attr):
    ret = []
    for attr in _attr:                  #Pour chaque attribut de la table, on regarde quels autres attributs il implique
        nec = [attr]
        n = []
        for col in _columns:
            if (col[0] == attr):
                n.append(col)
        csq = []
        for c1 in _columns:
            if (c1 not in n):
                c1InCsq = True
                i = 1
                while (i < len(n[0])):                  #On regarde pour chaque ligne parmis toutes celles qui la suivent si, même une seule fois, les 2 lignes sont les mêmes pour l'attribut "nécessaire" de la DF et pas pour le deuxième attribut
                    j = 1
                    while (i+j < len(n[0])):
                        bool1 = True
                        for n1 in n:
                            if (n1[i] != n1[i+j]):
                                bool1 = False
                        if(bool1):
                            if(c1[i] != c1[i+j]):
                                c1InCsq = False
                        j+=1
                    i+=1
                if(c1InCsq):
                    csq.append(c1[0])               #Si ce n'est pas le cas, on peut dire que l'attribut implique c1[0] (le second attribut)
        if (csq):
            ret.append([_tabName,nec,csq])
    for attr1 in _attr:                             #Idem avec cette fois-ci deux attributs origines
        for attr2 in _attr[_attr.index(attr1)+1:]:
            if (attr1 != attr2):
                nec = [attr1,attr2]
                n = []
                for col in _columns:
                    if (col[0] == attr2 or col[0] == attr1):
                        n.append(col)
                csq = []
                for c1 in _columns:
                    if (c1 not in n):
                        c1InCsq = True
                        i = 1
                        while (i < len(n[0])):
                            j = 1
                            while (i+j < len(n[0])):
                                bool1 = True
                                for n1 in n:
                                    if (n1[i] != n1[i+j]):
                                        bool1 = False
                                if(bool1):
                                    if(c1[i] != c1[i+j]):
                                        c1InCsq = False
                                j+=1
                            i+=1
                        if(c1InCsq):
                            csq.append(c1[0])
            if (csq):
                ret.append([_tabName,nec,csq])
    for r1 in ret:              #Elimine les doublons de la liste
        i = ret.index(r1) + 1
        while (i < len(ret)):
            if (r1 == ret[i]):
                ret.pop(i)
                i-=1
            i+=1
    prob = getProblematicFD(_columns, ret)
    for p in prob:              #Enlève les DF qui ne sont pas correctes (redondantes ou conséquence logique)
        ret.remove(p[0])
    return ret
    
def getProblematicFD(_columns, _FDOnTable):
    ret = [] #On retourne une liste de tuple de la forme (df,raisonDeRejet)
    #df redondante
    for DF1 in _FDOnTable:
        for DF2 in _FDOnTable:
            for DF3 in _FDOnTable:
                if(DF1 != DF2 and DF2 != DF3 and DF1 != DF3):
                    nec1, nec2, nec3 = getNec(DF1), getNec(DF2), getNec(DF3)
                    csq1, csq2, csq3 = getCsq(DF1), getCsq(DF2), getCsq(DF3)
                    bool = True
                    for a in nec1:      #si tous les éléments de nec1 sont dans nec2 et que leurs conséquences sont les mêmes, alors DF2 est redondante (soit nec2 plus grande que nec1, soit totalement égale)
                        if (a not in nec2):
                            bool = False
                    if (bool and csq1 == csq2):
                        ret.append((DF2,"La DF est redondante"))
                    if (nec1 == nec3 and csq1 == nec2 and csq2 == csq3):    #Règle de transitivité (A->B,B->C,A->C : A->C est redondant)
                        ret.append((DF3,"La DF est déjà une conséquence logique"))
    #df pas respectée
    for FD in _FDOnTable:
        nec, csq = getNec(FD), getCsq(FD)
        n, c = [], []
        for col in _columns:
            if (col[0] in nec):
                n.append(col)
            elif (col[0] in csq):
                c.append(col)
        i = 1
        while (i < len(n[0])):              #On regarde pour chaque ligne toutes celles qui la suivent, si une fois les éléments pour les deux lignes sont égaux dans nec et pas dans csq, la DF est invalide
            j = 1
            while (i+j < len(n[0])):
                bool1 = True
                for n1 in n:
                    if (n1[i] != n1[i+j]):
                        bool1 = False
                if (bool1):
                    for c1 in c:
                        if (c1[i] != c1[i+j]):
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
def getAllPossibleKeys(_attr):       #Retourne toutes les clés possibles i.e. une combinaison de toutes les colonnes
    allKeysPoss = []
    s = list(_attr)
    for x in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)):
        if (len(x) != 0):               #La liste nulle ne nous intéresse pas
            if (len(x) == 1):
                x = [str(str(x)[2:-3])]
            else:
                x = list(x)
            allKeysPoss.append(x)
    return allKeysPoss
    
def copyAttr(_listAttr):                 #Fait une deepcopy d'une liste d'attributs
    ret = []
    for c in _listAttr:
        ret.append(c)
    return ret
    
def findKeys(_FDOnTable, _attr):             #retourne la liste des clés de la table sur base des DF
    allKeys = getAllPossibleKeys(_attr)
    ret = []
    for keyPoss in allKeys:
        actAttr = copyAttr(keyPoss)       #Cette liste ajoute les attributs "impliquée" par la clé au fur et à mesure des DF
        retry = True
        while (retry):
            retry = False
            for FD in _FDOnTable:
                nec = getNec(FD)
                csq = getCsq(FD)
                for c in actAttr:        #On regarde pour chaque attribut si il est dans les éléments nécessaire de la DF, si oui on supprime cet attribut
                    if (c in nec):
                        nec.remove(c)
                if (not nec):           #Si la liste des éléments nécessaires est vide, on peut dire que toutes les conditions sont respecétes et ajouté les éléments conséquences de la DF à notre liste de col
                    for c in csq:
                        if (c not in actAttr):
                            actAttr.append(c)
                            retry = True        #On relance après car on a désormais un ou plusieurs attributs supplémentaires, permettant de potentiellement respecter de nouvelles DF
        isKey = True
        for c in _attr:              #Vérifie si keyPoss est bien une clé i.e. elle "implique" toutes les colonnes de la table
            if (c not in actAttr):
                isKey = False
        if (isKey):
            ret.append(keyPoss)
    for key1 in ret:                    #On supprime les clés redondates (toute clé plus grande que key1 et qui contient key1)
        for key2 in ret[ret.index(key1):]:
            if (len(key1) < len(key2)):
                keyTmp = copyAttr(key1)
                for c in key1:
                    if (c in key2):
                        keyTmp.remove(c)
                if (not keyTmp):
                    ret.remove(key2)
    return ret
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def isTableinBCNFor3NF(_FDOnTable, _tableKeys):
    boolBCNF = True
    reasonNotBCNF = []
    bool3NF = True
    reasonNot3NF = []
    for FD in _FDOnTable:
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