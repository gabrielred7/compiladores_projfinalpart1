"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
#Classe do resultado em tempo real (Runtime)

class RTResultado:
    def __init__(self):
        self.valor = None
        self.erro = None

    def registro(self, res):
        if res.erro: self.erro = res.erro
        return res.valor
    
    def sucesso(self, valor):
        self.valor = valor
        return self
    
    def falha(self, erro):
        self.erro = erro
        return self
    
