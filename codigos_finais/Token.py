"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Classe usada para representar 
#cada token produzido pelo analisador léxico. 

class Token:
    def __init__(self, ttype, value):
        self.tipo_token = ttype
        self.valor_token = value

    def __repr__(self):
        if self.valor_token: return f'{self.tipo_token}:{self.valor_token}'
        return f'{self.tipo_token}'
