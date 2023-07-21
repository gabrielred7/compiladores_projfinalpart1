"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#classe No que pega o token do número correspondente, int ou hexa
class NumeroDeNos:
    def __init__(self, tok):
        self.tok = tok

        self.pos_ini = self.tok.pos_ini
        self.pos_fim = self.tok.pos_fim
    
    def __repr__(self):
        return f'{self.tok}'
    
#classe nó para operadores binários
class BinOpNo:
    def __init__(self, no_esq, op_tok, no_dir):
        self.no_esq = no_esq
        self.op_tok = op_tok
        self.no_dir = no_dir

        self.pos_ini = self.no_esq.pos_ini
        self.pos_fim = self.no_dir.pos_fim

    def __repr__(self):
        return f'({self.no_esq}, {self.op_tok}, {self.no_dir})'

#classe nó para operadores unários
class UnaryOpNo:
    def __init__(self, op_tok, no):
        self.op_tok = op_tok
        self.no = no

        self.pos_ini = self.op_tok.pos_ini
        self.pos_fim = self.op_tok.pos_fim

    def __repr__(self):
        return f'({self.op_tok}, {self.no})'
    
#classes para nós identificadores

class VarEntraNo:
    def __init__(self, var_nome_token):
        self.var_nome_token = var_nome_token

        self.pos_ini = self.var_nome_token.pos_ini
        self.pos_fim = self.var_nome_token.pos_fim


class VarAlocadoNo:
    def __init__(self, var_nome_token, valor_no):
        self.var_nome_token = var_nome_token
        self.valor_no = valor_no

        self.pos_ini = self.var_nome_token.pos_ini
        self.pos_fim = self.valor_no.pos_fim


#class para nó if
class IfNo:
    """
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_ini = self.cases[0][0].pos_ini
        self.pos_fim = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_fim
    """
    def __init__(self, condicao, bloco, elses=None):
        self.condicao = condicao
        self.bloco = bloco
        self.elses = elses
        
#Class para bloco
class BlocoNo:
    def __init__(self, cmds, pos_ini, pos_fim):
        self.cmds = cmds
        self.pos_ini = pos_ini
        self.pos_fim = pos_fim

class ElseNo:
    def __init__(self, exp_condicional, bloco):
        self.exp_condicional = exp_condicional
        self.bloco = bloco

class PrintNo:
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return f'print {self.exp}'

class WhileNo:
    def __init__(self, exp, bloco):
        self.exp = exp
        self.bloco = bloco

    def __repr__(self):
        return f'while {self.exp} {self.bloco}'