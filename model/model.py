import copy
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.solBest = None
        self.maxConto = None
        self.topPlayer = None
        self.grafo=nx.DiGraph()
        self.idMap={}
        self.maxSomma=None

    def creaGrafo(self,g):
        nodi=DAO.getNodi(g)
        self.grafo.add_nodes_from(nodi)
        for a in nodi:
            self.idMap[a.PlayerID]=a
        archi=DAO.getArchi(g)
        for a in archi:
            if a[2]>0:
                self.grafo.add_edge(self.idMap[a[1]],self.idMap[a[0]],peso=a[2])
            else:
                self.grafo.add_edge(self.idMap[a[0]],self.idMap[a[1]],peso=(a[2])*(-1))

        pass

    def getTopPlayer(self):
        self.maxSomma=0
        self.topPlayer=None
        for a in self.grafo.nodes:
            c= len(list(self.grafo.out_edges(a)))

            if c>self.maxSomma:
                self.maxSomma=c
                self.topPlayer=a
        lista=[]
        for a in self.grafo.out_edges(self.topPlayer,data=True):
            lista.append( (a[1],a[2]))
        return self.topPlayer,self.maxSomma,lista

    def getDetails(self):
        return len(self.grafo.nodes),len(self.grafo.edges)
    
    
    def cammino(self,k):
        self.solBest=[]
        self.maxConto=0
        self.k=k
        for start in self.grafo.nodes:
            self.ricorsione([start],start)
        for a in self.solBest:
            print(self.calcola2(a),a)

        print(self.maxConto,self.solBest)
        return self.solBest,self.maxConto

    def ricorsione(self, parziale, start):

        if self.isTerminale(parziale):
            c=self.calcola(parziale)
            if c> self.maxConto:
                self.maxConto=c
                self.solBest=copy.deepcopy(parziale)
        else:
            ammissibili = self.getAmmissibili(parziale, self.grafo.nodes)
            if len(parziale)<self.k:
                for a in ammissibili:
                    parziale.append(a)
                    self.ricorsione(parziale,a)
                    parziale.pop()
        
        pass

    def getAmmissibili(self, parziale, nodi):
        ammissibili=[]
        battuti=[]
        for a in parziale:
            for i in list(self.grafo.neighbors(a)):
                battuti.append(i)
        for a in nodi:
            if a not in battuti and a not in parziale:
                ammissibili.append(a)
        return ammissibili
        pass

    def isTerminale(self, parziale):
        if len(parziale)==self.k:
            return True
        else:
            return False
        pass

    def calcola(self, parziale):
        somma=0
        for a in parziale:
            for i in self.grafo.out_edges(a,data=True):
                somma+=i[2]["peso"]
            for i in self.grafo.in_edges(a,data=True):
                somma-=i[2]["peso"]
        return somma

    def calcola2(self, a):
        somma = 0
        for i in self.grafo.out_edges(a, data=True):
            somma += i[2]["peso"]
        for i in self.grafo.in_edges(a, data=True):
            somma -= i[2]["peso"]
        return somma






