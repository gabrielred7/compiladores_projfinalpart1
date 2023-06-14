"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
#classe para saber o nome de todas as variáveis e os seus valores
class TabelaSimbolo:
    def __init__(self):
        self.simbolos = {}
        self.pai = None

    def get(self, nome):
        valor = self.simbolos.get(nome, None)
        if valor == None and self.pai:
            return self.pai.get(nome)
        return valor
    
    def set(self, nome, valor):
        self.simbolos[nome] = valor

    def remove(self, nome):
        del self.simbolos[nome]