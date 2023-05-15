"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
from Token import TokenType

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.next()

    def error(self):
        raise Exception('Erro de sintaxe')
    
    #Responsável por iniciar a análise da entrada chamando o método parseExpression().
    def parse(self):
        return self.parseExpression()
    
    #Responsável por analisar a expressão, chamando outros métodos para analisar subexpressões quando necessário.   
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

    """
    O primeiro passo é verificar se o próximo token é um número (TokNumber) ou um parêntese aberto (OpenParen). Se for um número, o método exige() é chamado para consumir o token e retornar o valor numérico. Se for um parêntese aberto, a expressão entre parênteses é analisada chamando o método operacao() para obter o operador e os métodos parseExpression() para obter as subexpressões a e b. Finalmente, o método exige() é chamado para consumir o parêntese fechado. Se o próximo token não é um número nem um parêntese aberto, o método operacao() é chamado para obter o operador e os métodos parseExpression() são chamados para obter as subexpressões a e b.
    """

    #Verifica o tipo do próximo token e chama o método exige() para consumi-lo e retornar o valor.
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
            self.error()
    
    #Verifica se o próximo token tem a tag esperada
    def ver(self, tag):
        return self.token_atual.type == tag

    def exige(self, tag):
        if self.ver(tag):
            valor = self.token_atual.value
            self.token_atual = self.lexer.next()
            return valor
        else:
            self.error()
