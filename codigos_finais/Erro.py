"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

class Erro:
    def __init__(self, pos_ini, pos_fim, erro_nome, detalhes):
        self.pos_ini = pos_ini
        self.pos_fim = pos_fim
        self.erro_nome = erro_nome
        self.detalhes = detalhes

    def as_string(self):
        resultado = f'{self.erro_nome}: {self.detalhes}\n'
        resultado += f'linha {self.pos_ini.ln + 1}'
        return resultado

#Erro do processo do Lexer    
class CharIlegalErro(Erro):
    def __init__(self, pos_ini, pos_fim,detalhes):
        super().__init__(pos_ini, pos_fim,"Erro: Caracter ilegal", detalhes)    

#Erro do processo do Parser
class SintaxeInvalidaErro(Erro):
    def __init__(self, pos_ini, pos_fim,detalhes=''):
        super().__init__(pos_ini, pos_fim,'Sintaxe Inválida',detalhes)