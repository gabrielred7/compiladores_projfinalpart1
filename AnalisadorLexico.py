"""
Trabalho de Compiladores - Projeto Pt1: Analisador Lexico
Nome: Gabriel Almeida Mendes - DRE: 117204959
"""

import re
import sys
"""
OBS: Professor eu nao conseguir fazer esse programa usando expressoes regulares, forma que acredito que voce queria, pq nunca fui bom com manipulação de strings
"""

#Classe usada para representar cada token produzido pelo analisador léxico. 
class Token:
    def __init__(self, ttype, value):
        self.tipo_token = ttype
        self.valor_token = value

#Classe que implementa o analisador léxico. 
class Lexer:
    def __init__(self, text):
        self.entrada = text
        self.posicao = 0
        self.char_atual = self.entrada[self.posicao]

    def error(self):
        raise Exception('Caractere inválido')

    # O método "avancar" leva o ponteiro para o próximo caractere
    def avancar(self):
        self.posicao += 1
        self.char_atual = self.entrada[self.posicao] if self.posicao < len(self.entrada) else None

    # Ignora espaços em branco (como space, tab e etc)
    def pular_espacoBranco(self):
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
        number = ''
        while self.char_atual is not None and self.char_atual.isdigit():
            number += self.char_atual
            self.avancar()
        return int(number)

    def hexadecimal(self):
        number = ''
        while self.char_atual is not None and self.char_atual.isalnum():
            number += self.char_atual
            self.avancar()
        if number.startswith('0x'):
            return int(number[:2], 16)
        else:
            self.error()

    def operadores(self):
        op = self.char_atual
        self.avancar()
        if op == '+':
            return Token('TokOp', 'OpSum')
        elif op == '-':
            return Token('TokOp', 'OpSub')
        elif op == '*':
            return Token('TokOp', 'OpMult')
        elif op == '/':
            return Token('TokOp', 'OpDiv')
        elif op == '%':
            return Token('TokOp', 'OpMod')
        elif op == '^':
            return Token('TokOp', 'OpExp')
        else:
            self.error()

    # Lê o caractere atual e retorna o proximo token
    def next(self):
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.pular_espacoBranco()
                continue
            
            elif self.char_atual == '/':
                if self.verificar() == '/':
                    self.pular_comentario_linha()
                    continue
                elif self.verificar() == '*':
                    self.avancar()
                    self.avancar()
                    self.pular_comentario_bloco()
                    continue

            elif self.char_atual.isdigit():
                return Token('TokNumber', self.decimal())
            
            elif self.char_atual == '0':
                self.avancar()
                if self.char_atual == 'x':
                    self.avancar()
                    return Token('TokNumber', self.hexadecimal())
                else:
                    return Token('TokNumber', 0)
                
            elif self.char_atual in ('+', '-', '*', '/', '%', '^'):
                return self.operadores()
            
            else:
                self.error()

        return Token('TokEOF', None)


def main():
    texto_entrada = sys.stdin.read()
    lexer = Lexer(texto_entrada)
    while True:
        token = lexer.next()
        if token.tipo_token == 'TokEOF':
            break #Fim dos arquivos
        print(token.tipo_token, token.valor_token)


if __name__ == '__main__':
    main()