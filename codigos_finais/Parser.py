"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
##Alerta! Estamos fazendo implementando a tarefa opcional

import Lexer
import ParserResultado
import NumeroDeNos
import Erro
import Token

#Classe que implementa o parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.avancar()

    def avancar(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.token_atual = self.tokens[self.tok_idx]
        return self.token_atual
    
    #Responsável por chamar as expressões e retornar 
    def parse(self):
        res = self.expr()
        if not res.erro and self.token_atual.tipo_token != Lexer.TT_EOF:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim, 
                "Espera-se '^', '*', '/', '+' ou '-' " 
            ))
        return res
    

    #Métodos da gramática: (Ainda incompletos)
    def fator(self):
        res = ParserResultado.ParserResultado()
        tok = self.token_atual

        if tok.tipo_token in (Lexer.TT_PLUS, Lexer.TT_MINUS):
            res.registro(self.avancar())
            fator = res.registro(self.fator())
            if res.erro: return res
            return res.sucesso(NumeroDeNos.UnaryOpNo(tok, fator))
        
        elif tok.tipo_token in (Lexer.TT_INT, Lexer.TT_HEXA):
            res.registro(self.avancar())
            return res.sucesso(NumeroDeNos.NumeroDeNos(tok))
        
        elif tok.tipo_token == Lexer.TT_LPAREN:
            res.registro(self.avancar())
            expr = res.registro(self.expr())
            if res.erro: return res
            if self.token_atual.tipo_token == Lexer.TT_RPAREN:
                res.registro(self.avancar())
                return res.sucesso(expr)
            else:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, 
                    self.token_atual.pos_fim, "Espera-se ')'"))

        return res.falha(Erro.SintaxeInvalidaErro(
            tok.pos_ini, tok.pos_fim, 'Espera-se int ou hexa'))

    def termo(self):
        return self.bin_op(self.fator, (
            Lexer.TT_EXP, Lexer.TT_MUL, Lexer.TT_DIV))

    
    def expr(self):
        return self.bin_op(self.termo, (
            Lexer.TT_PLUS, Lexer.TT_MINUS))
    
    

    def bin_op(self, func, ops):
        res = ParserResultado.ParserResultado()
        esq = res.registro(func())
        if res.erro: return res

        while self.token_atual.tipo_token in ops:
            op_tok = self.token_atual
            res.registro(self.avancar())
            dir = res.registro(func())
            if res.erro: return res
            esq = NumeroDeNos.BinOpNo(esq, op_tok, dir)

        return res.sucesso(esq)