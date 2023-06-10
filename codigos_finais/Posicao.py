"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Classe para representar a posição do Token
class Posicao:
    def __init__(self, idx, ln, col, txt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.txt = txt


    #O método avançar recebe o char atual e avança
    #o index e a col. Se o char atual == \n
    #avança a linha

    """
    #O método avançar recebe o char atual e avança o index e a col. 
    Se o char atual == \n avança a linha
    """

    def avancar(self, char_atual=None):
        self.idx += 1
        self.col += 1
        if char_atual == '\n':
            self.ln += 1
            self.col = 0
        return self
    
    #O método copia retorna a posição
    def copia(self):
        return Posicao(self.idx, self.ln, self.col, self.txt)