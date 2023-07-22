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
import ParserResultado
import Interpretador
import Contexto
import TabelaSimbolo
import Numero
import NumeroDeNos


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
    ast = parser.parser_programa()
    if ast.erro: return None, ast.erro

    res = ParserResultado.ParserResultado()
    salvar_ast_em_arquivo("programa.ara", ast)
    """
    #Gera o interpretador
    interpretador = Interpretador.Interpretador()
    contexto = Contexto.Contexto('<programa>')
    contexto.tabela_simbolo = tabela_Simbolos_Global
    resultado = interpretador.visita(ast.no, contexto)
    """
    #return resultado.valor, resultado.erro
    return ast.no, ast.erro
    #return tokens, erros

def serialize_ast(node, output_file):
    with open(output_file, 'w') as file:
        serialize_node(node, file)

def serialize_node(node, file):
    if node is None:
        return

    file.write(f"{node.type} {node.value} {len(node.children)}\n")
    for child in node.children:
        serialize_node(child, file)
        
import os

def salvar_ast_em_arquivo(arquivo_saida, parser_resultado):
    # Verifica se ocorreram erros durante a análise sintática e semântica
    if parser_resultado.erro:
        print("Ocorreu um erro durante a análise sintática ou semântica.")
        return

    # Verifica se há uma AST armazenada no resultado do parser
    if not parser_resultado.no:
        print("A AST não foi gerada corretamente.")
        return

    ast = parser_resultado.no  # Obtém a AST do objeto ParserResultado

    # Obtém o diretório do código em execução
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Concatena o nome do arquivo ao diretório para obter o caminho completo
    caminho_arquivo = os.path.join(diretorio_atual, arquivo_saida)

    with open(caminho_arquivo, 'w') as f:
        for node in ast:
            tipo = node['type']
            if tipo == 'funcao':
                nome_funcao = node['nome']
                num_argumentos = node['num_argumentos']
                num_var_locais = node['num_var_locais']
                f.write(f"FUNCTION {nome_funcao} {num_argumentos} {num_var_locais}\n")
            elif tipo == 'comando':
                comando = node['comando']
                if comando == 'RETURN':
                    f.write("RETURN\n")
                elif comando == 'NUMBER':
                    valor = node['valor']
                    f.write(f"NUMBER {valor}\n")
                elif comando == 'ADD':
                    f.write("ADD\n")
                elif comando == 'SUB':
                    f.write("SUB\n")
                # Adicione outras instruções aqui conforme necessário
            # Adicione outros tipos de nós do AST aqui conforme necessário

    print(f"AST salva no arquivo: {caminho_arquivo}")





def main():

    
    while True:
        texto = input()
        resultado, erros = run(texto)
        if erros: print(erros.as_string())
        elif resultado: print(resultado)

main()