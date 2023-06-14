"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Classe que pega o contexto atual do programa,
#seja uma função, ou até mesmo o programa inteiro
class Contexto:
    def __init__(self, display_nome, pai=None, pai_entrando_pos=None):
        self.display_nome = display_nome
        self.pai = pai
        self.pai_entrando_pos = pai_entrando_pos
        self.tabela_simbolo = None

