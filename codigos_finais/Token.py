"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

from enum import Enum

#Classe usada para representar cada token produzido pelo analisador léxico. 

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# A classe TokenType é uma enumeração que define os tipos de tokens que podem aparecer na gramática.

class TokenType(Enum):
    TokNumber = 1
    OpenParen = 2
    CloseParen = 3
    OpSum = 4
    OpSub = 5
    OpMult = 6
    OpDiv = 7
    OpExp = 8
    TokEOF = 9