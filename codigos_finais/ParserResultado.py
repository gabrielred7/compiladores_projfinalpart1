"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
#Classe para checar se tem algum erro
class ParserResultado:
    def __init__(self):
        self.erro = None
        self.no = None
        self.ultimo_registro_De_avanco = 0
        self.count_avanca = 0

    #Registro para avanços
    def registro_de_avanco(self):
        self.ultimo_registro_De_avanco += 1
        self.count_avanca += 1

    ##Checa se tem erro no resultado. Se sim,
    #Ele é alocado para a class erro.
    def registro(self, res):
        self.count_avanca += res.count_avanca
        if res.erro: self.erro = res.erro
        return res.no

    #Retorna o Nó se sucesso
    def sucesso(self, no):
        self.no = no
        return self
    
    #Retorna um erro 
    def falha(self, erro):
        if not self.erro or self.count_avanca == 0:
            self.erro = erro
        return self