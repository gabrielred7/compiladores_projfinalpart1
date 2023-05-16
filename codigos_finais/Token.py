"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
"""
Classe usada para representar cada token produzido pelo analisador léxico. 
Pega a posição do token para mostrar onde ele tá caso ocorra algum erro.
"""

class Token:
    def __init__(self, ttype, value=None, pos_ini = None, pos_fim = None):
        self.tipo_token = ttype
        self.valor_token = value

        if pos_ini:
            self.pos_ini = pos_ini.copia()
            self.pos_fim = pos_ini.copia()
            self.pos_fim.avancar()

        if pos_fim:
            self.pos_fim = pos_fim

    def __repr__(self):
        if self.valor_token: return f'{self.tipo_token}:{self.valor_token}'
        return f'{self.tipo_token}'