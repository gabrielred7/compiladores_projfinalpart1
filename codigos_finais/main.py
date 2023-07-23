"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal

import Lexer
import Parser

def run(texto):
    # Generate tokens
		lexer = Lexer.Lexer(texto)
		tokens, erro = lexer.next()
		if erro: return None, erro
		
		# Generate AST
		parser = Parser.Parser(tokens)
		ast = parser.parser_programa()

		return ast.no, ast.erro


def main():
    while True:
        texto = input()
        resultado, erros = run(texto)
        if erros: print(erros.as_string())
        elif resultado: print(resultado)


main()