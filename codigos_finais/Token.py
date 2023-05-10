import re
import sys

#Classe usada para representar cada token produzido pelo analisador léxico. 
class Token:
    def __init__(self, ttype, value):
        self.tipo_token = ttype
        self.valor_token = value