from enum import Enum

class TokenType(Enum):
    TokNumber = 1
    OpenParen = 2
    CloseParen = 3
    OpSum = 4
    OpSub = 5
    OpMult = 6
    OpDiv = 7
    OpExp = 8
    TokEOF = 9

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.next()

    def parse(self):
        return self.parseExpression()

    def parseExpression(self):
        if self.ver(TokenType.TokNumber):
            num = self.exige(TokenType.TokNumber)
            return num
        elif self.ver(TokenType.OpenParen):
            self.exige(TokenType.OpenParen)
            op = self.operacao()
            a = self.parseExpression()
            b = self.parseExpression()
            self.exige(TokenType.CloseParen)
            return (op, a, b)
        else:
            op = self.operacao()
            a = self.parseExpression()
            b = self.parseExpression()
            return (op, a, b)

    def operacao(self):
        if self.ver(TokenType.OpSum):
            return self.exige(TokenType.OpSum)
        elif self.ver(TokenType.OpSub):
            return self.exige(TokenType.OpSub)
        elif self.ver(TokenType.OpMult):
            return self.exige(TokenType.OpMult)
        elif self.ver(TokenType.OpDiv):
            return self.exige(TokenType.OpDiv)
        elif self.ver(TokenType.OpExp):
            return self.exige(TokenType.OpExp)
        else:
            raise ValueError("Token inválido")

    def ver(self, tag):
        return self.token_atual.type == tag

    def exige(self, tag):
        if self.ver(tag):
            valor = self.token_atual.value
            self.token_atual = self.lexer.next()
            return valor
        else:
            raise ValueError(f"Token {tag} esperado, mas {self.token_atual.type} encontrado")

"""
Nesse código, a classe TokenType é uma enumeração que define os tipos de tokens que podem aparecer na gramática. A classe Parser recebe um objeto lexer que é responsável por extrair os tokens da entrada. O método parse() é responsável por iniciar a análise da entrada chamando o método expr().

O método expr() é responsável por analisar a expressão, chamando outros métodos para analisar subexpressões quando necessário. O primeiro passo é verificar se o próximo token é um número (TokenType.NUM) ou um parêntese aberto (TokenType.OPEN_PAREN). Se for um número, o método exige() é chamado para consumir o token e retornar o valor numérico. Se for um parêntese aberto, a expressão entre parênteses é analisada chamando o método op() para obter o operador e os métodos expr() para obter as subexpressões esquerda e direita. Finalmente, o método exige() é chamado para consumir o parêntese fechado.

Se o próximo token não é um número nem um parêntese aberto, o método op() é chamado para obter o operador e os métodos expr() são chamados para obter as subexpressões esquerda e direita.

O método op() simplesmente verifica o tipo do próximo token e chama o método exige() para consumi-lo e retornar o valor.

O método ver() verifica se o próximo token tem a tag esperada. Se sim, retorna True. Se não, retorna False.
"""