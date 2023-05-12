class TokenType:
    def __init__(self, tag):
        self.tag = tag

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def parse(self):
        return self.expression()

    def expression(self):
        if self.current_token.type.tag == 'NUM':
            num = self.current_token.value
            self.current_token = self.lexer.next_token()
            return num
        elif self.current_token.type.tag == 'LPAREN':
            self.current_token = self.lexer.next_token()
            result = self.expression()
            self.exige('RPAREN')
            self.current_token = self.lexer.next_token()
            return result
        elif self.current_token.type.tag in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER']:
            op = self.current_token.type.tag
            self.current_token = self.lexer.next_token()
            left = self.expression()
            right = self.expression()
            return [op, left, right]
        else:
            raise ValueError('Invalid token')

    def ver(self, tag):
        return self.current_token.type.tag == tag

    def exige(self, tag):
        if self.ver(tag):
            self.current_token = self.lexer.next_token()
        else:
            raise ValueError(f'Expected {tag}, found {self.current_token.type.tag}')

"""
A classe TokenType apenas define um tipo de token com uma tag, enquanto a classe Token guarda o valor de um token e seu tipo.

A classe Parser é responsável por analisar a entrada de acordo com a gramática especificada. O método parse() é responsável por iniciar o processo de análise da expressão, enquanto o método expression() é responsável por analisar cada parte da expressão de acordo com a gramática.

O método ver(tag) verifica se o próximo token tem a tag especificada. Já o método exige(tag) verifica se o próximo token tem a tag especificada e avança para o próximo token se sim, ou gera um erro caso contrário.

O código assume que o lexer possui um método next_token() que retorna o próximo token da entrada. Além disso, a função raise ValueError gera um erro com uma mensagem personalizada.
"""