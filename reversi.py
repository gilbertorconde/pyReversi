'''
Created on 17 de Jul de 2012

@author: gil
'''
#import subprocess
#import platform
import copy
from records import Records

class Reversi(object):
    '''
    Reversi -> Cria o objecto que implementa o jogo "Reversi". Um jogo de tabuleiro simples
    e representado por caracteres em consola.
    '''

    def _trocaTurno(self):
        estado = ' # ' if self.estado == ' 0 ' else ' 0 '
        self.estado = estado
        self.nestado = ' # ' if estado == ' 0 ' else ' 0 '
        
        
    def _actualizaPossibilidades(self):
        
        def _aplicaIfens(lin,col,i,j):
            if self._verificaArea(lin+(i*2), col+(j*2)) and self.reversiMatrix[lin+i][col+j] == self.nestado:
                if self.reversiMatrix[lin+(i*2)][col+(j*2)] == '   ':
                    self.reversiMatrix[lin+(i*2)][col+(j*2)] = ' - '
                    return
                if self.reversiMatrix[lin+i][col+j] == '   ':
                    return
                if self.reversiMatrix[lin+(i*2)][col+(j*2)] == self.nestado:
                    _aplicaIfens(lin+i, col+j, i, j)
                    return
            return


        for i in range(self.dimLinhas):
            for j in range(self.dimColunas):
                if self.reversiMatrix[i][j] == ' - ':
                    self.reversiMatrix[i][j] = '   '
    
        for lin in range(self.dimLinhas):
            for col in range(self.dimColunas):
                if self.reversiMatrix[lin][col] == self.estado:
                    for i in range(-1,2):
                        for j in range(-1,2):
                            _aplicaIfens(lin, col, i, j)
            
            

    def _verificaArea(self, linha, coluna):
        if linha < self.dimLinhas and linha >= 0 and coluna < self.dimColunas and coluna >= 0:
            return True
        return False
 
    def _aplicaJogada(self, linha, coluna):
        
        def _trocaEstado(lin, col, i, j):
            if self._verificaArea(lin+(i*2), col+(j*2)) and self.reversiMatrix[lin+i][col+j] == self.nestado:
                if self.reversiMatrix[lin+(i*2)][col+(j*2)] == self.estado:
                    self.reversiMatrix[lin+i][col+j] = self.estado
                    return
                if self.reversiMatrix[lin+(i*2)][col+(j*2)] == '   ':
                    return
                if self.reversiMatrix[lin+(i*2)][col+(j*2)] == self.nestado:
                    _trocaEstado(lin+i, col+j, i, j)
                    if self.reversiMatrix[lin+(i*2)][col+(j*2)] == self.estado:
                        self.reversiMatrix[lin+i][col+j] = self.estado
                    return
            return
        
        if self.reversiMatrix[linha][(ord(coluna)-ord('a'))] != ' - ':
            return 'invalido'
        else:
            col = (ord(coluna)-ord('a'))
            lin = linha
            self.reversiMatrix[lin][col] = self.estado
            
            for i in range(-1,2):
                for j in range(-1,2):
                    _trocaEstado(lin, col, i, j)
            
            self.JogadaTemp = [lin,col,self.estado[1]]
            return 'continua'
    
    def _atualizaPontos(self):
        z = 0
        c = 0
        a = 0
        for i in range(self.dimLinhas):
            for j in range(self.dimColunas):
                if self.reversiMatrix[i][j] == ' 0 ':
                    z += 1
                if self.reversiMatrix[i][j] == ' # ':
                    c += 1
                if self.reversiMatrix[i][j] == ' - ':
                    a += 1
        self.zero = z
        self.charp = c
        return a
            
    def _processaComando(self, jogada):
        if jogada == 'N':
            return 'novo'
        elif jogada == 'F':
            return 'sair'
        elif jogada =='U':
            if self.last != None:
                return 'refazer'
            return 'nrefazer'
        elif jogada == 'T':
            self.clear()
            #print(self.recs)
            self.msgText = self.recs.getRecordsTableStr()
            self.msg = True
            print(self)
            self.msg = False
            self._input("\nPrima [enter] para continuar...")
            return
        elif jogada == 'H':
            self.clear()
            self.msg = True
            self.msgText ="""\nN – (Novo jogo) Recomeça uma nova partida considerando derrota do jogador corrente.
F – (Fim) Após confirmação do utilizador, termina o jogo e o programa.
U – (Undo) Desfaz a última jogada, dando hipótese do jogador anterior jogar novamente. Com este comando deve ser possível
desfazer mais do que uma jogada.
T – (Tabela Top 10) Apresenta a tabela dos 10 melhores jogos realizados indicando o número de peças de cada jogador e o nome
do vencedor, sendo o melhor jogo o que teve mais peças do jogador vencedor. Esta tabela poderá ser atualizada no final de
um jogo com mais peças do vencedor que as do último da tabela, sendo necessário perguntar o nome do vencedor.
H – (Help) Apresenta todos os comandos indicando a letra e a descrição sumária de cada um.\n\n""" 
            print(self)
            self.msg = False
            self._input("Prima [enter] para continuar...")
            return
        
        try:
            if len(jogada) == 2 or len(jogada) == 3:
                linha = (int(jogada[0]) - 1) if len(jogada) == 2 else ((int(jogada[0])*10)+int(jogada[1])-1)
                coluna = str(jogada[1]) if len(jogada) == 2 else str(jogada[2])
                if not self._verificaArea(linha,(ord(coluna)-ord('a'))):
                    return 'invalido'
                self._guardaEstadoActual()
                return self._aplicaJogada(linha,coluna)
            else:
                return 'invalido'
        except:
            return 'invalido'
    
    def _iniciarVariaveis(self):
        self.reversiMatrix = [ [ "   " for i in range(self.dimLinhas) ]
                               for j in range(self.dimColunas) ]

        self.reversiMatrix[int(self.dimLinhas/2)][int(self.dimColunas/2)] = ' 0 '
        self.reversiMatrix[int(self.dimLinhas/2)-1][int(self.dimColunas/2)-1] = ' 0 '
        self.reversiMatrix[int(self.dimLinhas/2)-1][int(self.dimColunas/2)] = ' # '
        self.reversiMatrix[int(self.dimLinhas/2)][int(self.dimColunas/2)-1] = ' # '
        ## VARIAVEIS DE SCORE ##
        self.recs = Records("MPDS.rve",self.recNum)
        self.charp = 2
        self.zero = 2
        self.estado = ' # '
        self.nestado = ' 0 '
        self.mensagem = "Inicio do jogo. # é o primeiro jogador. Para ajuda digite H\n"
        self.JogadaTemp = None
        self.last = None
        self.msgText = ""
        self.msg = False
    
    def _refazer(self):
        
        self.reversiMatrix = self.last.reversiMatrix
        self.charp = self.last.charp
        self.zero = self.last.zero
        self.estado = self.last.estado
        self.nestado = self.last.nestado
        self.mensagem = self.last.mensagem
        self.JogadaTemp = self.last.JogadaTemp
        self.last = self.last.last
    
    def _guardaEstadoActual(self):
        self.last = copy.copy(self)
        self.last.reversiMatrix = [ [ "   " for i in range(self.dimLinhas) ]
                               for j in range(self.dimColunas) ]
        for i in range(self.dimLinhas):
            for j in range(self.dimColunas):
                self.last.reversiMatrix[i][j] = str(self.reversiMatrix[i][j])
    
    def __str__(self):
        if self.msg == True:
            return self.msgText
        #os.system('clear')
        self.clear()
        strStruct = self.mensagem + '\n'
        if self.reversiMatrix == None:
            return self
        strStruct += '    '
        for idd in range(self.dimColunas):
            strStruct += " "+chr(idd+(ord('a')))+"  "
        strStruct += "\n"
        strStruct += "    "+(("--- ")*(self.dimColunas))+"\n"
        for i in range(self.dimLinhas):
            strStruct += str(i+1)
            strStruct += "  |" if i+1<10 else " |"
            for j in range(self.dimColunas):
                strStruct += self.reversiMatrix[i][j]+"|"
            strStruct += "\n"
            if i != self.dimLinhas-1:
                strStruct += "   +"+(("---+")*(self.dimColunas))+"\n"
        strStruct += "    "+(("--- ")*(self.dimColunas))+"\n"
        return strStruct
    
    def __init__(self, dimLinhas, dimColunas, recNum):
        '''
        Recebe como parametros as dimensões da matriz que compões o numero de linhas
        e colunas da grelha do jogo.
        '''
        self.dimLinhas = dimLinhas
        self.dimColunas = dimColunas
        self.recNum = recNum
        self._iniciarVariaveis()
        
    def iniciarJogo(self):
        while True:
            varEstado = self._iniciarCiclo()
            if varEstado == 'novo':
                self._iniciarVariaveis()
                continue
            if varEstado == 'sair':
                break
        
    def _porRecords(self):
        self.clear()
        aux = 0
        if not self.zero == self.charp:
            pontos = self.zero if self.zero > self.charp else self.charp 
            if self.recs.isFull() and pontos < self.recs.getLastRecord():
                aux = -1
            vencedor = '0' if self.zero > self.charp else '#'
            self.msg = True
            self.msgText = "O Jogador '"+vencedor+"' ganhou a partida." 
            print(self)
            self.msg = False
            if aux != -1:
                self.recs.putRecord(self._input("Qual o seu nome? "), pontos)

    def _iniciarCiclo(self):
        endedGame = False
        aux = -1
        self._actualizaPossibilidades()
        while True:
            if endedGame:
                break
            if self.JogadaTemp != None: ## Atribui os '()' à jogada temporaria
                self.reversiMatrix[self.JogadaTemp[0]][self.JogadaTemp[1]] = "("+self.JogadaTemp[2]+")"
            print(self)
            if self.JogadaTemp != None: ## Retira os '()' à jogada temporaria apos print()
                self.reversiMatrix[self.JogadaTemp[0]][self.JogadaTemp[1]] = " "+self.JogadaTemp[2]+" "
            if aux == 0:
                self._porRecords()
                self._input("para recomeçar prima [enter]")
                return 'novo'
            jogada = self._input("("+str(self.charp)+","+str(self.zero)+") "+str(self.estado[1])+">")
            estado = self._processaComando(jogada)
            if estado == 'novo' or estado == 'sair':
                self._porRecords()
                strAux = " jogo" if estado == 'novo' else " do jogo"
                self._input("\nPrima [enter] para "+estado+strAux)
                return estado
            if estado == 'invalido':
                self.mensagem = "Jogada inválida, proximo jogador -> "+self.nestado[1]
                self._trocaTurno()
                self._actualizaPossibilidades()
                aux = self._atualizaPontos()
                continue
            if estado == 'continua':
                self._trocaTurno()
                self._actualizaPossibilidades()
                self.mensagem = "Jogada válida, proximo jogador -> "+self.estado[1]
                aux = self._atualizaPontos()
                continue
            if estado == 'refazer':
                self._refazer()
                aux = self._atualizaPontos()
                self.mensagem = "Refazer jogada, proximo jogador -> "+self.estado[1]
                continue
            if estado == 'nrefazer':
                self.mensagem = "Não existem jogadas anteriores. Proximo jogador -> "+self.nestado[1]
                continue

    def _input(self, mensagem):
        return input(mensagem)

    def clear(self):
        return ## Não está implementado
    
        