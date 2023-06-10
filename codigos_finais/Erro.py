"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
import Posicao

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

#Erro do processo do parser
class SintaxeInvalidaErro(Erro):
    def __init__(self, pos_ini, pos_fim, detalhes=''):
        super().__init__(pos_ini, pos_fim,'Sintaxe Inválida', detalhes)

#Erro em tempo de execução
class RTErro(Erro):
    def __init__(self, pos_ini, pos_fim, detalhes, contexto):
        super().__init__(pos_ini, pos_fim, 'Runtime erro', detalhes)
        self.contexto = contexto

    def as_string(self):
        resultado = self.gera_traceback()
        resultado += f'{self.erro_nome}: {self.detalhes}'
        return resultado
    
    def gera_traceback(self):
        resultado = ''
        pos = self.pos_ini
        ctx = self.contexto

        while ctx:
            resultado = f' line {str(pos.ln + 1)}, in {ctx.display_nome}\n' + resultado
            pos = ctx.pai_entrando_pos
            ctx = ctx.pai

        return 'Traceback recente: \n' + resultado