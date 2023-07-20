"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal

import sys
import Lexer
import Erro
import Parser
import Interpretador
import Contexto
import TabelaSimbolo
import Numero

tabela_Simbolos_Global = TabelaSimbolo.TabelaSimbolo()
tabela_Simbolos_Global.set("FALSO", Numero.Numero(0))
tabela_Simbolos_Global.set("VERDADEIRO", Numero.Numero(1))

def run(texto):
    #Gera tokens
    lexer = Lexer.Lexer(texto)
    tokens, erros = lexer.next()
    if erros: return None, erros

    # Gera a AST
    parser = Parser.Parser(tokens)
    ast = parser.parse()
    if ast.erro: return None, ast.erro

    #Gera o interpretador
    interpretador = Interpretador.Interpretador()
    contexto = Contexto.Contexto('<programa>')
    contexto.tabela_simbolo = tabela_Simbolos_Global
    resultado = interpretador.visita(ast.no, contexto)

    return resultado.valor, resultado.erro
    #return ast.no, ast.erro
    #return tokens, erros
def main():

    
    while True:
        texto = input()
        resultado, erros = run(texto)
        if erros: print(erros.as_string())
        elif resultado: print(resultado)

main()