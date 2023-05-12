from enum import Enum


class TokenType(Enum):
    TokNumber = 1
    OpSum = 2
    OpSub = 3
    OpMult = 4
    OpDiv = 5
    OpExp = 6
    TokLParen = 7
    TokRParen = 8
    TokEOF = 9


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.next()

    def parse(self):
        return self.parseExpression()

    def parseExpression(self):
        if self.ver(TokenType.TokNumber):
            return self.exige(TokenType.TokNumber).value
        elif self.ver(TokenType.TokLParen):
            self.exige(TokenType.TokLParen)
            result = self.parseExpression()
            self.exige(TokenType.TokRParen)
            return result
        elif self.ver(TokenType.OpSum):
            self.exige(TokenType.OpSum)
            left = self.parseExpression()
            right = self.parseExpression()
            return left + right
        elif self.ver(TokenType.OpSub):
            self.exige(TokenType.OpSub)
            left = self.parseExpression()
            right = self.parseExpression()
            return left - right
        elif self.ver(TokenType.OpMult):
            self.exige(TokenType.OpMult)
            left = self.parseExpression()
            right = self.parseExpression()
            return left * right
        elif self.ver(TokenType.OpDiv):
            self.exige(TokenType.OpDiv)
            left = self.parseExpression()
            right = self.parseExpression()
            return left / right
        elif self.ver(TokenType.OpExp):
            self.exige(TokenType.OpExp)
            left = self.parseExpression()
            right = self.parseExpression()
            return left ** right
        else:
            raise Exception("Token invalido")

    def ver(self, tag):
        return self.token_atual.tag == tag

    def exige(self, tag):
        if self.ver(tag):
            token = self.token_atual
            self.token_atual = self.lexer.next()
            return token
        else:
            raise Exception(f'Esperado {tag}, encontrado {self.token_atual}')



"""
Nessa implementação, a classe TokenType é uma enumeração que representa os tipos de token possíveis para a parseExpressionessão aritmética, e a classe Parser é responsável por implementar as regras da gramática e realizar a análise sintática da parseExpressionessão. O construtor da classe recebe um objeto lexer, que é responsável por transformar a entrada em tokens, e o método parse é responsável por iniciar o processo de análise sintática chamando o método parseExpression.

O método parseExpression implementa as regras da gramática para a parseExpressionessão aritmética. Primeiro, ele verifica se o próximo token é um número ou um parêntese esquerdo, e retorna o valor numérico ou inicia a análise de uma nova parseExpressionessão dentro dos parênteses. Caso contrário, ele verifica se o próximo token é um operador aritmético e chama a função correspondente para calcular o resultado da operação.

O método ver verifica se o próximo token tem a tag esperada, e o método exige consome o próximo token caso ele tenha a tag esperada ou lança uma exceção caso contrário.

Essa implementação assume que a entrada é válida de acordo com a gramática especificada. Caso a entrada não seja válida, uma exceção será lançada com a mensagem "Erro de sintaxe".
"""