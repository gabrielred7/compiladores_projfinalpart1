"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
#Classe para checar se tem algum erro
class ParserResultado:
    def __init__(self):
        self.erro = None
        self.no = None

    def registro(self, res):
        if isinstance(res, ParserResultado):
            if res.erro: self.erro = res.erro
            return res.no

        return res
    
    def sucesso(self, no):
        self.no = no
        return self
    
    def falha(self, erro):
        self.erro = erro
        return self