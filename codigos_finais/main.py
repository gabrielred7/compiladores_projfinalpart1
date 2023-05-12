"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal

import sys
import Lexer
import Parser

def main():
    texto_entrada = sys.stdin.read()
    lexer = Lexer(texto_entrada)
    while True:
        token = lexer.next()
        if token.tipo_token == 'TokEOF':
            break #Fim dos arquivos
        print(token.tipo_token, token.valor_token)
    parser = Parser(lexer)
    resultado = parser.parseExpression()
    print("Resultado:", resultado)

if __name__ == '__main__':
    main()

"""
Para utilizar a classe Parser, basta instanciá-la com um objeto da classe Lexer.
Em seguida, chamar o método parseExpression() da classe Parser passando a entrada como argumento.
"""