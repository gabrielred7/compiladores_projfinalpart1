"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal

import Lexer
import Parser
import ParserResultado
import CodeGenerator  # Importe o módulo CodeGenerator
import json

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
    texto = input()
    res, erros = run(texto)
    if erros: 
        print(erros.as_string())
    elif res:
        # Cria a instância do CodeGenerator
        code_generator = CodeGenerator.CodeGenerator()

        # Gera as instruções de bytecode a partir da AST
        code_generator.generate(res)

        # Obtém as instruções de bytecode
        instructions = code_generator.get_instructions()

        # Salva as instruções em um arquivo usando a função serialize_instructions
        with open('programa.arac', 'w') as file:
            json.dump(instructions, file)

        # Imprime as instruções na tela (opcional)
        print(instructions)

main()