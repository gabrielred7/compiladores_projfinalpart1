"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
import Erro

#Classe para guardar números e fazer operações com outros números
class Numero:
    def __init__(self, valor):
        self.valor = valor
        self.set_pos()
        self.set_contexto()

    def set_pos(self, pos_ini=None, pos_fim=None):
        self.pos_ini = pos_ini
        self.pos_fim = pos_fim
        return self
    
    def set_contexto(self, contexto=None):
        self.contexto = contexto
        return self
    
    def somado(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor + 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def subtraido(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor - 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def multiplicado(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor * 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def dividido(self, outro):
        if isinstance(outro, Numero):
            if outro.valor == 0:
                return None, Erro.RTErro(
                    outro.pos_ini, outro.pos_fim,
                    'Divisão por zero',
                    self.contexto
                )
             
            return Numero(self.valor / 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def exponenciado(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor ** 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def get_comparado_Eq(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor == 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def get_comparado_Neq(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor != 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def get_comparado_MenorQue(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor < 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def get_comparado_MaiorQue(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor > 
                          outro.valor).set_contexto(
                self.contexto
                          ), None

    def get_comparado_MenorEqQue(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor <= 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def get_comparado_MaiorEqQue(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor >= 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def E(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor and 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def Ou(self, outro):
        if isinstance(outro, Numero):
            return Numero(self.valor or 
                          outro.valor).set_contexto(
                self.contexto
                          ), None
        
    def Nao(self):
        return Numero(1 if self.valor == 0 else 0).set_contexto(self.contexto), None

    def copia(self):
        copia = Numero(self.valor)
        copia.set_pos(self.pos_ini, self.pos_fim)
        copia.set_contexto(self.contexto)
        return copia 

    def is_true(self):
        return self.valor != 0

    def __repr__(self):
        return str(self.valor)
        
