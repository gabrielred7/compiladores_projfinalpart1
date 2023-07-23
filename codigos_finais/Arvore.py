"""
Trabalho de Compiladores - Projeto de Compiladores - Tarefa 2
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

import json
import NumeroDeNos
# Classe para representar a árvore sintática
class Arvore:
    def __init__(self, no):
        self.no = no

# Função para salvar a AST em um arquivo no formato JSON
def salvar_ast_em_arquivo(arvore_sintatica, nome_arquivo):
    # Converte a AST para uma estrutura em dicionário para facilitar a serialização em JSON
    def converter_para_dicionario(no):
        if isinstance(no, NumeroDeNos.NumeroDeNos):
            return {
                'tipo': 'NumeroDeNos',
                'tok': str(no.tok)
            }
        elif isinstance(no, NumeroDeNos.BinOpNo):
            return {
                'tipo': 'BinOpNo',
                'no_esq': converter_para_dicionario(no.no_esq),
                'op_tok': str(no.op_tok),
                'no_dir': converter_para_dicionario(no.no_dir)
            }
        elif isinstance(no, NumeroDeNos.UnaryOpNo):
            return {
                'tipo': 'UnaryOpNo',
                'op_tok': str(no.op_tok),
                'no': converter_para_dicionario(no.no)
            }
        elif isinstance(no, NumeroDeNos.VarEntraNo):
            return {
                'tipo': 'VarEntraNo',
                'var_nome_token': str(no.var_nome_token)
            }
        elif isinstance(no, NumeroDeNos.VarAlocadoNo):
            return {
                'tipo': 'VarAlocadoNo',
                'var_nome_token': str(no.var_nome_token),
                'valor_no': converter_para_dicionario(no.valor_no)
            }
        elif isinstance(no, NumeroDeNos.IfNo):
            if no.elses:
                return {
                    'tipo': 'IfNo',
                    'condicao': converter_para_dicionario(no.condicao),
                    'bloco': converter_para_dicionario(no.bloco),
                    'elses': [converter_para_dicionario(else_no) for else_no in no.elses]
                }
            else:
                return {
                    'tipo': 'IfNo',
                    'condicao': converter_para_dicionario(no.condicao),
                    'bloco': converter_para_dicionario(no.bloco)
                }
        elif isinstance(no, NumeroDeNos.WhileNo):
            return {
                'tipo': 'WhileNo',
                'exp': converter_para_dicionario(no.exp),
                'bloco': converter_para_dicionario(no.bloco)
            }
        elif isinstance(no, NumeroDeNos.FunCallNo):
            return {
                'tipo': 'FunCallNo',
                'no_para_chamar': converter_para_dicionario(no.no_para_chamar),
                'no_args': [converter_para_dicionario(arg) for arg in no.no_args]
            }
        elif isinstance(no, NumeroDeNos.FuncDefNo):
            return {
                'tipo': 'FuncDefNo',
                'var_nome_tok': str(no.var_nome_tok),
                'arg_nome_toks': [str(arg_tok) for arg_tok in no.arg_nome_toks],
                'corpo_no': converter_para_dicionario(no.corpo_no)
            }
        elif isinstance(no, NumeroDeNos.PrintNo):
            return {
                'tipo': 'PrintNo',
                'exp': converter_para_dicionario(no.exp)
            }
        elif isinstance(no, NumeroDeNos.BlocoNo):
            return {
                'tipo': 'BlocoNo',
                'comandos': [converter_para_dicionario(cmd) for cmd in no.comandos]
            }
        elif isinstance(no, NumeroDeNos.ElseNo):
            return {
                'tipo': 'ElseNo',
                'exp_condicional': converter_para_dicionario(no.exp_condicional),
                'bloco': converter_para_dicionario(no.bloco)
            }
        elif isinstance(no, NumeroDeNos.FuncNo):
            return {
                'tipo': 'FuncNo',
                'nome': str(no.nome),
                'args': [converter_para_dicionario(arg) for arg in no.args],
                'corpo': converter_para_dicionario(no.corpo),
                'contexto': converter_para_dicionario(no.contexto)
            }
        elif isinstance(no, NumeroDeNos.DeclaracaoNo):
            return {
                'tipo': 'DeclaracaoNo',
                'var_nome': str(no.var_nome),
                'exp': converter_para_dicionario(no.exp)
            }
        elif isinstance(no, NumeroDeNos.ListaDeFuncoes):
            return {
                'tipo': 'ListaDeFuncoes',
                'funcoes': [converter_para_dicionario(func) for func in no.funcoes]
            }

    # Converte a árvore sintática em um dicionário
    arvore_dict = converter_para_dicionario(arvore_sintatica.no)

    # Salva o dicionário em um arquivo JSON
    with open(nome_arquivo, 'w') as arquivo_json:
        json.dump(arvore_dict, arquivo_json, indent=2)
