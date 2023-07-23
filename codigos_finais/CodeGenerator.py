""""
    Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
from enum import Enum
import json

class OpCode(Enum):
    EXIT = 0
    NUMBER = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    POW = 6
    NOT = 7
    NEG = 8
    EQ = 9
    NEQ = 10
    LE = 11
    LEQ = 12
    GE = 13
    GEQ = 14
    LOAD = 15
    STORE = 16
    POP = 17
    DUP = 18
    PRINT = 19
    JUMP = 20
    JUMP_TRUE = 21
    JUMP_FALSE = 22

class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, node):
        if node is None:
            return

        node_type = node.__class__.__name__
        if node_type == 'NumeroDeNos':
            self.instructions.append({'op': OpCode.NUMBER.value, 'value': int(node.tok.valor)})
        elif node_type == 'BinOpNo':
            self.generate(node.no_esq)
            self.generate(node.no_dir)
            if node.op_tok.tipo == 'MAIS':
                self.instructions.append({'op': OpCode.ADD.value})
            elif node.op_tok.tipo == 'MENOS':
                self.instructions.append({'op': OpCode.SUB.value})
            elif node.op_tok.tipo == 'MULTIPLICA':
                self.instructions.append({'op': OpCode.MUL.value})
            elif node.op_tok.tipo == 'DIVIDE':
                self.instructions.append({'op': OpCode.DIV.value})
            elif node.op_tok.tipo == 'POW':
                self.instructions.append({'op': OpCode.POW.value})
            elif node.op_tok.tipo == 'IGUAL':
                self.instructions.append({'op': OpCode.EQ.value})
            elif node.op_tok.tipo == 'DIFERENTE':
                self.instructions.append({'op': OpCode.NEQ.value})
            elif node.op_tok.tipo == 'MENOR':
                self.instructions.append({'op': OpCode.LE.value})
            elif node.op_tok.tipo == 'MENORIGUAL':
                self.instructions.append({'op': OpCode.LEQ.value})
            elif node.op_tok.tipo == 'MAIOR':
                self.instructions.append({'op': OpCode.GE.value})
            elif node.op_tok.tipo == 'MAIORIGUAL':
                self.instructions.append({'op': OpCode.GEQ.value})
        elif node_type == 'UnaryOpNo':
            self.generate(node.no)
            if node.op_tok.tipo == 'MENOS_UNARIO':
                self.instructions.append({'op': OpCode.NEG.value})
            elif node.op_tok.tipo == 'NOT':
                self.instructions.append({'op': OpCode.NOT.value})
        # Adicione aqui outras classes de nós conforme necessário

    def get_instructions(self):
        return self.instructions

def serialize_instructions(instructions, output_file):
    with open(output_file, 'w') as file:
        json.dump(instructions, file)

