"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Arquivo principal
import Lexer
import Erro
import Parser
import Interpretador
import Contexto
import Parser


def run(texto):
    lexer = Lexer.Lexer(texto)
    tokens, erros = lexer.next()
    if erros: return None, erros

    # Gera a AST
    parser = Parser.Parser(tokens)
    ast = parser.parse()

    if ast.erro: return None, ast.erro

    interpretador = Interpretador.Interpretador()
    contexto = Contexto.Contexto('<programa>')
    resultado = interpretador.visita(ast.no, contexto)

    return resultado.valor, resultado.erro
    #return ast.no, ast.erro
    #return tokens, erros
def main():

    


    return ast.no, ast.erro
    #return tokens, erros
def main():

    while True:
        texto = input()
        resultado, erros = run(texto)
        if erros: print(erros.as_string())
        print(resultado)

main()