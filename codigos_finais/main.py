"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal

import sys
import Lexer
import Erro

def run(texto):
    lexer = Lexer.Lexer(texto)
    tokens, erros = lexer.next()

    return tokens, erros

def main():
    #texto_entrada = sys.stdin.read()
    #lexer = Lexer(input())
    
    while True:
        texto = input()
        resultado, erros = run(texto)
        #if token.tipo_token == 'TokEOF':
        #    break #Fim dos arquivos
        #print(token.tipo_token, token.valor_token)
        if erros: print(erros.as_string())
        print(resultado)

#if __name__ == '__main__':
main()