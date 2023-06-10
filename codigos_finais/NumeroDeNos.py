"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#classe No que pega o número, int ou hexa
class NumeroDeNos:
    def __init__(self, tok):
        self.tok = tok

        self.pos_ini = self.tok.pos_ini
        self.pos_fim = self.tok.pos_fim
    
    def __repr__(self):
        return f'{self.tok}'
    
#classe no para operadores
class BinOpNo:
    def __init__(self, no_esq, op_tok, no_dir):
        self.no_esq = no_esq
        self.op_tok = op_tok
        self.no_dir = no_dir

        self.pos_ini = self.no_esq.pos_ini
        self.pos_fim = self.no_dir.pos_fim

    def __repr__(self):
        return f'({self.no_esq}, {self.op_tok}, {self.no_dir})'

class UnaryOpNo:
    def __init__(self, op_tok, no):
        self.op_tok = op_tok
        self.no = no

        self.pos_ini = self.tok.pos_ini
        self.pos_fim = self.tok.pos_fim

    def __repr__(self):
        return f'({self.op_tok}, {self.no})'