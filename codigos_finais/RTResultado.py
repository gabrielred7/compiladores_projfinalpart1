"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
#Classe do resultado em tempo real (Runtime)
#Checa os resultados e erros
class RTResultado:
    def __init__(self):
        self.valor = None
        self.erro = None

    #Checa se tem erro no resultado. Se sim,
    #Ele é alocado para a class erro.
    def registro(self, res):
        if res.erro: self.erro = res.erro
        return res.valor
    
    def sucesso(self, valor):
        self.valor = valor
        return self
    
    def falha(self, erro):
        self.erro = erro
        return self
    
