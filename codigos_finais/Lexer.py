"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

import Token
import Posicao
import Erro
"""
OBS: Professor não conseguimos fazer esse programa usando expressoes regulares, forma que acredito que voce queria, entao usamosfuncoes como o int() para converter para hexadecimal, por exemplo. Somado a isso estamos com dificuldades de fazer isso funcionar, estavamos seguindo um exemplo do livro do dragão entao acredito que esteja certo, mas não consigo obter uma saida clara

"""

#CONSTANTES
DIGITOS = '0123456789'

#TOKENS

TT_INT		= 'TokNumber'
TT_PLUS     = 'TokOp OpSum'
TT_MINUS    = 'TokOp OpSub'
TT_MUL      = 'TokOp OpMul'
TT_DIV      = 'TokOp OpDiv'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'


#Classe que implementa o analisador léxico. 
class Lexer:
    def __init__(self, text):
        self.entrada = text
        self.posicao = Posicao.Posicao(-1, 0, -1, text)
        self.char_atual = None
        self.avancar()

    def error(self):
        raise Exception('Caractere inválido')

    # O método avancar atribui a entrada ao char atual
    def avancar(self):
        self.posicao.avancar(self.char_atual)
        self.char_atual = self.entrada[self.posicao.idx] if self.posicao.idx < len(self.entrada) else None

    # Ignora espaços em branco (como space, tab e etc)
    def pular_espaco_branco(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()
    
    # Ignora caracteres de comentarios
    def pular_comentario_linha(self):
        while self.char_atual is not None and self.char_atual != '\n':
            self.avancar()
        self.avancar()
    
    def pular_comentario_bloco(self):
        while self.char_atual is not None:
            if self.char_atual == '*' and self.verificar() == '/':
                self.avancar()
                self.avancar()
                break
            else:
                self.avancar()

    #Auxilia na verificação dos caracteres de comentarios
    def verificar(self):
        self.verificar_posicao = self.posicao + 1
        return self.entrada[self.verificar_posicao] if self.verificar_posicao < len(self.entrada) else None

    def decimal(self):
        numero = ''
        while self.char_atual is not None and self.char_atual in DIGITOS:
            numero += self.char_atual
            self.avancar()
        return Token.Token(TT_INT, int(numero))

    def hexadecimal(self):
        numero = ''
        while self.char_atual is not None and (self.char_atual.isdigit() or self.char_atual.isalpha()):
            numero += self.char_atual
            self.avancar()
        if numero.startswith('0x'):
            return int(numero, 16)
        else:
            self.error()

    def operadores(self):
        op = self.char_atual
        self.avancar()
        if op == '+':
            return Token.Token('TokOp', 'OpSum')
        elif op == '-':
            return Token.Token('TokOp', 'OpSub')
        elif op == '*':
            return Token.Token('TokOp', 'OpMult')
        elif op == '/':
            return Token.Token('TokOp', 'OpDiv')
        elif op == '%':
            return Token.Token('TokOp', 'OpMod')
        elif op == '^':
            return Token.Token('TokOp', 'OpExp')
        else:
            self.error()

    # Lê o caractere atual e retorna o proximo token
    def next(self):
        tokens = []

        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.avancar()

            elif self.char_atual == '/':
                if self.verificar() == '/':
                    self.pular_comentario_linha()
                    self.avancar()
                elif self.verificar() == '*':
                    self.avancar()
                    self.avancar()
                    self.pular_comentario_bloco()
                    self.avancar()

            elif self.char_atual in DIGITOS:
                tokens.append(self.decimal())
            
            elif self.char_atual == '0':
                self.avancar()
                if self.char_atual == 'x':
                    self.avancar()
                    return Token.Token('TokNumber', self.hexadecimal())
                else:
                    return Token.Token('TokNumber', 0)
                
            elif self.char_atual in ('+', '-', '*', '/', '%', '^'):
                return self.operadores()
            
            else:
                self.error()

        return tokens, None
