"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
import Posicao

class Erro:
    def __init__(self, linha, erro_nome, detalhes):
        self.linha = Posicao.Posicao.ln
        self.erro_nome = erro_nome
        self.detalhes = detalhes

    def as_string(self):
        resultado = f'{self.erro_nome}: {self.detalhes}\n'
        resultado += f'linha {self.linha.ln}'
        return resultado
    
class CharIlegalErro(Erro):
    def __init__(self, linha, erro_nome, detalhes):
        super().__init__(linha, erro_nome, "Erro: Caracter ilegal", detalhes)    
        