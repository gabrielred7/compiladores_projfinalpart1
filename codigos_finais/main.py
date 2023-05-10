"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal

import sys
import Lexer

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