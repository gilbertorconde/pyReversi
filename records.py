'''
Created on 18 de Jul de 2012

@author: gil
'''
from ioRecordsFile import RWFile

class Records(object):
    '''
    classdocs
    '''


    def __init__(self, ficheiro, recNumber):
        '''
        Constructor
        '''
        self.varAux = '~'
        self.recNumber = recNumber
        self.nome = None
        self.pontos = None
        if ficheiro != None:
            self.ioFile = RWFile(ficheiro)
            aux = self.ioFile.reedFileToStr()
            val = aux.split(self.varAux)
            if val[0] != 'ERR':
                self.nome = []
                self.pontos = []
                for i in range(0,len(val)-1,2):
                    self.nome.append(val[i])
                    self.pontos.append(int(val[i+1]))
    
    def _escreveNoFicheiro(self):
        
        aux = ""
        
        for i in range(len(self.pontos)):
            aux += self.nome[i]+self.varAux+str(self.pontos[i])
            if i != (len(self.pontos)-1):
                aux += self.varAux
        self.ioFile.writeStrToFile(aux)
        
        return
    
    def __str__(self):
        return self.getRecordsTableStr()
    
            
    def getRecordsTableStr(self):
        returnStr = "\n OS "+str(self.recNumber)+" MELHORES RESULTADOS \n\n"
        
        if self.pontos == None:
            return returnStr+"Sem Records até ao momento \n"
        returnStr += "o------o--------------------------o------o\n"
        returnStr += "|  Nº  |           NOME           | Pts  |\n"
        returnStr += "o------+--------------------------+------o\n"
        for i in range(len(self.pontos)):
            returnStr += '| '+(str(i+1)+'º'+(' '*3))[:4:]+" | "+(self.nome[i]+(" "*24))[:24:]+" | "+(str(self.pontos[i])+(' '*4))[:4:]+" |\n"
        returnStr += "o------o--------------------------o------o\n"
        return returnStr+"\n"
    
    
    def getRecords(self):
        return list(zip(self.pontos, self.nome))
    
    def putRecord(self, nome, pontos):
        
        def _limpaAMais():
            while len(self.pontos) > self.recNumber:
                self.pontos.pop(-1)
                self.nome.pop(-1)
        
        if self.pontos == None:
            self.pontos = []
            self.nome = []
            self.pontos.insert(0, pontos)
            self.nome.insert(0, nome)
            _limpaAMais()
            self._escreveNoFicheiro()
            return
        
        for i in range(len(self.pontos)):
            if pontos > self.pontos[i]:
                self.pontos.insert(i, pontos)
                self.nome.insert(i, nome)
                _limpaAMais()
                self._escreveNoFicheiro()
                return
            try:
                if pontos == self.pontos[i] and pontos != self.pontos[i+1]:
                    self.pontos.insert(i+1, pontos)
                    self.nome.insert(i+1, nome)
                    _limpaAMais()
                    self._escreveNoFicheiro()
                    return
            except:
                pass
        if len(self.pontos) < self.recNumber:
            self.pontos.append(pontos)
            self.nome.append(nome)
        _limpaAMais()
        self._escreveNoFicheiro()
        return
        
    def isFull(self):
        return True if len(self.pontos) == self.recNumber else False  
    
    def getLastRecord(self):
        return self.pontos[-1]