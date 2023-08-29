import numpy as np
import matplotlib.pyplot as plt

class ling_term:
    def __init__(self, n: str, t: str, r: list):
        self.__name = n
        self.__type = t
        self.__range = r

    def getName(self): return self.__name  
    def getType(self): return self.__type
    def getInter(self): return self.__range

    def relevance(self, x: float):
        if self.__type == 'triangular':
            if x > self.__range[0] and x <= self.__range[1]: return (x-self.__range[0])/(self.__range[1]-self.__range[0])
            elif x >= self.__range[1] and x <= self.__range[2]: return (self.__range[2]-x)/(self.__range[2]-self.__range[1])
            else: return 0
        
        elif self.__type == 'trapezoidal':
            if x > self.__range[0] and x <= self.__range[1]: return (x-self.__range[0])/(self.__range[1]-self.__range[0])
            if x >= self.__range[1] and x <= self.__range[2]: return 1
            elif x >= self.__range[2] and x <= self.__range[3]: return (self.__range[3]-x)/(self.__range[3]-self.__range[2])
            else: return 0

        elif self.__type == "gaussian":
            if x >= (self.__range[0]-self.__range[1]) and x <= (self.__range[0]+self.__range[1]): return np.exp( -( (x-self.__range[0])**2 )/(self.__range[2]**2) )
            else : return 0

class ling_var:

    def __init__(self, n: str, r: list):
        self.__name = n
        self.__range = r 
        self.__terms = []

    def getName(self): return self.__name
    def getRange(self): return self.__range
    def getTerms(self): return self.__terms

    def add(self, n, t, r):
        lt = ling_term(n, t, r)
        self.__terms.append(lt)

    def showTerms(self):
        names = [ i.getName() for i in self.__terms]
        return names
    
    def plot(self):
        for i in self.__terms:
            aux = [ i.relevance(j) for j in self.__range ]
            plt.plot(self.__range, aux, label = i.getName() )
        plt.title( self.__name )
        plt.legend() 
        plt.show() 

class controller:

    def __init__(self, r: list, vetlv: list, v: list):
        self.__rules = r
        self.__vetlv = vetlv 
        self.__values = v 
        self.__rulesbase = [] 
        self.__splitRules()
        self.__map()
        self.__activate()

    def __splitRules(self):
        for i in self.__rules: self.__rulesbase.append( i.split() )

    def __map(self):
        then = [ i.index('então') for i in self.__rulesbase ]

        m = []
        aux = []
        k = 0 
        for i in self.__rulesbase:
            for j in i[0 : then[k] : 2]:
                aux.append( self.__vetlv[k].showTerms().index(j) )
                k += 1
            m.append(aux)
            aux = []
            k = 0

        aux1 = []
        aux2 = []
        k = 0
        for i in m:
            for j in i:
                aux1.append( self.__vetlv[k].getTerms()[j].relevance( self.__values[k] ) )
                k += 1
            aux2.append(aux1)
            aux1 = []
            k = 0 
        return aux2 
    
    def __activate(self):
        rules_activated = []
        for i in range( len(self.__map()) ):
            if not all( k==0 for k in self.__map()[i] ): rules_activated.append(i)
        return rules_activated
    
    def mamdani(self, defuzzy = 'centroid'):
        lt = 0
        aux = 0
        aux1 = []
        aux2 = []
        for ra in self.__activate():
            while aux < len(self.__rulesbase[ra]) - 2:
                index = self.__vetlv[lt].showTerms().index(self.__rulesbase[ra][aux])
                aux1.append( self.__vetlv[lt].getTerms()[index].relevance(self.__values[lt]) )
                aux += 2
                lt += 1
            aux2.append(min(aux1))
            lt,aux = 0,0
            aux1 = []

        aux1 = []
        aux3  = []
        k = 0
        for ra in self.__activate():
            index = self.__vetlv[-1].showTerms().index(self.__rulesbase[ra][-1])
            for i in self.__vetlv[-1].getRange(): 
                if self.__vetlv[-1].getTerms()[index].relevance(i) <= aux2[k] :aux1.append( self.__vetlv[-1].getTerms()[index].relevance(i) )
                else: aux1.append( aux2[k] )
            aux3.append(aux1)
            aux1 = []
            k += 1

        aux1 = []
        k,j=0,0
        while k < len(aux3[0]):
            aux = 0
            for j in aux3: aux = max(j[k],aux)
            aux1.append(aux)
            k += 1

        aux3.append(aux1)

        if defuzzy == "centroid":
            ct = self.__vetlv[-1].getRange() * np.array(aux3[-1])
            return sum(ct)/sum(np.array(aux3[-1]))
        
        if defuzzy == "center of gravity":
            hmax = max(aux3[-1])
            i = self.__vetlv[-1].getRange()[ aux3[-1].index(hmax) ]
            k = aux3[-1].index(hmax)
            f = i
            while aux3[-1][k] <= aux3[-1][k+1]: 
                f = self.vetvl[-1].universo[ k+1 ]
                k +=1
            return (i+f)/2
        
        if defuzzy == 'max average':
            hmax = max(aux3[-1])
            i = self.__vetlv[-1].getRange()[ aux3[-1].index(hmax) ]
            k = aux3[-1].index(hmax)
            n = 0
            f = i
            while aux3[-1][k] <= aux3[-1][k+1]: 
                f += self.__vetlv[-1].getRange()[ k+1 ]
                k +=1
                n +=1
            return f/n
