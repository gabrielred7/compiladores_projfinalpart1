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

#################################################
#  Metodos das regras da gramática:
    
    def fator(self):
        res = ParserResultado.ParserResultado()
        tok = self.token_atual

        if tok.tipo_token in (Lexer.TT_PLUS, Lexer.TT_MINUS):
            res.registro_de_avanco()
            self.avancar()
            fator = res.registro(self.fator())
            if res.erro: return res
            return res.sucesso(NumeroDeNos.UnaryOpNo(tok, fator))
        
        return self.pot()
    

    def termo(self):
        return self.bin_op(self.fator, (
            Lexer.TT_EXP, Lexer.TT_MUL, Lexer.TT_DIV))

    
    def expr(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual.E_igual(Lexer.TT_KEYWORD, 'VAR'):
            res.registro_de_avanco()
            self.avancar()

            if self.token_atual.tipo_token != Lexer.TT_ID:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, self.token_atual.pos_fim,
                    "Espera-se identificador"
                ))
            
            var_nome = self.token_atual
            res.registro_de_avanco()
            self.avancar()

            if self.token_atual.tipo_token != Lexer.TT_EQ:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, self.token_atual.pos_fim,
                    "Espera-se '='"
                ))
            
            res.registro_de_avanco()
            self.avancar()
            expr = res.registro(self.expr())
            if res.erro: return res
            return res.sucesso(NumeroDeNos.VarAlocadoNo(var_nome,
                                                        expr))

        no = res.registro(self.bin_op(self.comp_expr, (
            (Lexer.TT_KEYWORD, 'AND'), (Lexer.TT_KEYWORD, 'OR'))))

        if res.erro:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini,
                self.token_atual.pos_fim,
                "Espera-se 'VAR, int, hex, id, '+', '-' or '('"
            ))
        
        return res.sucesso(no)
    
    def atom(self):
        res = ParserResultado.ParserResultado()
        tok = self.token_atual

        if tok.tipo_token in (Lexer.TT_INT, Lexer.TT_HEXA):
            res.registro_de_avanco()
            self.avancar()
            return res.sucesso(NumeroDeNos.NumeroDeNos(tok))
        
        elif tok.tipo_token == Lexer.TT_ID:
            res.registro_de_avanco()
            self.avancar()
            return res.sucesso(NumeroDeNos.VarEntraNo(tok))
        
        elif tok.tipo_token == Lexer.TT_LPAREN:
            res.registro_de_avanco()
            self.avancar()
            expr = res.registro(self.expr())
            if res.erro: return res
            if self.token_atual.tipo_token == Lexer.TT_RPAREN:
                res.registro_de_avanco()
                self.avancar()
                return res.sucesso(expr)
            else:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, self.token_atual.pos_fim,
                    "Espera-se ')' "
                ))
        elif tok.E_igual(Lexer.TT_KEYWORD, 'IF'):
            if_expr = res.registro(self.if_expr())
            if res.erro: return res
            return res.sucesso(if_expr)


        return res.falha(Erro.SintaxeInvalidaErro(
            tok.pos_ini, tok.pos_fim,
            "Espera-se int, hexa, id, '+', '-', '('"
        ))
    
    def if_expr(self):
        res = ParserResultado.ParserResultado()
        cases = []
        else_case = None
        tok = self.token_atual

        if not self.token_atual.E_igual(Lexer.TT_KEYWORD, 'IF'):
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
                f"Espera-se 'IF'"
            ))
        
        res.registro_de_avanco()
        self.avancar()
        #expr = res.registro(self.expr())
        condicao = res.registro(self.expr())
        if res.erro: return res

        
        if tok.tipo_token == Lexer.TT_LBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro(
                tok.pos_ini, tok.pos_fim,
                f"Espera-se Abre chaves" 
            ))
        """
        if tok.tipo_token == Lexer.TT_LBLOCO:
            res.registro_de_avanco()
            self.avancar()
            expr = res.registro(self.expr())
            if res.erro: return res
            cases.append((condicao, expr))
            if self.token_atual.tipo_token == Lexer.TT_RBLOCO:
                res.registro_de_avanco()
                self.avancar()
                return res.sucesso(expr)
            else:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, self.token_atual.pos_fim,
                    "Espera-se '}' "
                ))
        """
        res.registro_de_avanco()
        self.avancar()

        expr = res.registro(self.expr())
        if res.erro: return res
        cases.append((condicao, expr))
        
        if not tok.tipo_token == Lexer.TT_RBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro(
                tok.pos_ini, tok.pos_fim,
                f"Espera-se Fecha chaves" 
            ))
        
        while tok.E_igual(Lexer.TT_KEYWORD, 'ELIF'):
            res.registro_de_avanco()
            self.avancar()

            condicao = res.registro(self.expr())
            if res.erro: return res

            if not tok.tipo_token == Lexer.TT_LBLOCO:
                return res.falha(Erro.SintaxeInvalidaErro(
                tok.pos_ini, tok.pos_fim,
                f"Espera-se Abre chaves" 
            ))

            res.registro_de_avanco()
            self.avancar()

            expr = res.registro(self.expr())
            if res.erro: return res
            cases.append((condicao, expr))

            if not tok.tipo_token == Lexer.TT_RBLOCO:
                return res.falha(Erro.SintaxeInvalidaErro(
                    tok.pos_ini, tok.pos_fim,
                    f"Espera-se Fecha chaves" 
                ))

        if tok.E_igual(Lexer.TT_KEYWORD, 'ELSE'):
            res.registro_de_avanco()
            self.avancar()

            else_case = res.registro(self.expr())
            if res.erro: return res

        return res.sucesso(NumeroDeNos.IfNo(cases, else_case))



    def pot(self):
        return self.bin_op(self.atom, (Lexer.TT_EXP, ), self.fator)

    def expr_Aritm(self):
        return self.bin_op(self.fator, ( Lexer.TT_PLUS, Lexer.TT_MINUS))
    
    def comp_expr(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual.E_igual(Lexer.TT_KEYWORD, 'NOT'):
            op_tok = self.token_atual
            res.registro_de_avanco()
            self.avancar()

            no = res.registro(self.comp_expr())
            if res.erro: return res
            return res.sucesso(NumeroDeNos.UnaryOpNo(op_tok, no))
        
        no = res.registro(self.bin_op(self.expr_Aritm,
                                      (Lexer.TT_2EQ, Lexer.TT_MAIOREQQUE,
                                        Lexer.TT_MAIORQUE, Lexer.TT_MENOREQQUE,
                                          Lexer.TT_MENORQUE, Lexer.TT_NEQ)))

        if res.erro:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
                "Espera-se int, hex, id, '+', '-' or '(' or 'NOT'" 
            ))
        
        return res.sucesso(no)

#####################################################

#Checa os tokens que podem ser aceitos
    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParserResultado.ParserResultado()
        esq = res.registro(func_a())
        if res.erro: return res

        while self.token_atual.tipo_token in ops or (self.token_atual.tipo_token, 
         self.token_atual.valor_token) in ops:
            op_tok = self.token_atual
            res.registro_de_avanco()
            self.avancar()
            dir = res.registro(func_b())
            if res.erro: return res
            esq = NumeroDeNos.BinOpNo(esq, op_tok, dir)

        return res.sucesso(esq)