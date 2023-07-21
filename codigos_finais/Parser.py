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
        res = self.parser_bloco()
        if not res.erro and self.token_atual.tipo_token != Lexer.TT_EOF:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim, 
                "Espera-se '^', '*', '/', '+' ou '-' " 
            ))
        return res
    
    #Programa -> Funcs
    def parser_programa(self):
        res = self.parser_funcs()

        if not res.erro and self.token_atual.tipo_token != Lexer.TT_EOF:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim, 
                "Ocorreu alguma falha" 
            ))
        return res


#################################################
#  Metodos das regras da gramática:
    # Lista de funções (zero ou mais, sem separador)
    #Funcs -> {FuncDef}
    def parser_funcs(self):
        funcs = []
        while self.token_atual == Lexer.TT_KEYWORD and self.token_atual.E_igual(Lexer.TT_KEYWORD, 'fun'):
            res = self.parser_funcdef()
            if res.erro:
                return res
            funcs.append(res.valor)
        return ParserResultado.ParserResultado().sucesso(funcs)

    #FuncDef -> 'fun' NOME '(' Args ')' Bloco
    def parser_funcdef(self):
        
        res = ParserResultado.ParserResultado()

        if not self.token_atual.E_igual(Lexer.TT_KEYWORD, 'fun'):
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, "'fun' esperado"))
        
        res.registro_de_avanco()
        self.avancar()

        if self.token_atual.tipo_token != Lexer.TT_ID:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "Nome da função esperado"))
        
        nome_func = self.token_atual.valor_token
        res.registro_de_avanco()
        self.avancar()

        if self.token_atual.tipo_token != Lexer.TT_LPAREN:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "'(' esperado"))
        res.registro_de_avanco()
        self.avancar()
        resultado_args = self.parser_args()
        if resultado_args.erro: return resultado_args

        if self.token_atual.tipo_token != Lexer.TT_RPAREN:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "')' esperado"))
        res.registro_de_avanco()
        self.avancar()

        resultado_bloco = self.parser_bloco()
        if resultado_bloco.erro:return resultado_bloco

        return res.sucesso(NumeroDeNos.FuncDefNo(
            nome_func, 
            resultado_args, resultado_bloco))

    """
     # Lista de nomes (zero ou mais, separado por vírgula)
        Args -> 
        Args -> NOME {',' NOME}
    """
    def parser_args(self):
        res = ParserResultado.ParserResultado()
        args = []

        if self.token_atual.tipo_token == Lexer.TT_ID:
            args.append(self.token_atual.valor_token)
            res.registro_de_avanco()
            self.avancar()

            while self.token_atual.tipo_token == Lexer.TT_COMMA:
                res.registro_de_avanco()
                self.avancar()
                
                if self.token_atual.tipo_token != Lexer.TT_ID:
                    return res.falha(Erro.SintaxeInvalidaErro(
                        self.token_atual.pos_ini, 
                        self.token_atual.pos_fim, 
                        "Nome da variável esperado"))
                args.append(self.token_atual.valor_token)
                res.registro_de_avanco()
                self.avancar()
        
        return res.sucesso(args)
    """
    # Lista de expressões (zero ou mais, separadas por vírgula)
    Exps -> 
    Exps -> Exp {',' Exp} 
    """
    def parser_exps(self):
        res = ParserResultado.ParserResultado()
        exps = []

        if self.token_atual.tipo_token == Lexer.TT_RPAREN:
            return res.sucesso(exps)
        res.registro_de_avanco()
        self.avancar()
        exp = res.registro(self.parser_expr())
        if res.erro: return res
        res.registro_de_avanco()
        self.avancar()

        exps.append(exp)

        while self.token_atual.tipo_token == Lexer.TT_COMMA:
            res.registro_de_avanco()
            self.avancar()
            exp = res.registro(self.parser_expr())
            if res.erro:return res
            exps.append(exp)

        return res.sucesso(exps)


    def fator(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual.tipo_token in (Lexer.TT_PLUS, Lexer.TT_MINUS):
            res.registro_de_avanco()
            self.avancar()
            fator = res.registro(self.fator())
            if res.erro: return res
            return res.sucesso(NumeroDeNos.UnaryOpNo(self.token_atual, fator))
        
        return self.pot()
    

    def termo(self):
        return self.bin_op(self.fator, (
            Lexer.TT_EXP, Lexer.TT_MUL, Lexer.TT_DIV))

    
    def expr(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual.E_igual(Lexer.TT_KEYWORD, 'var'):
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
            (Lexer.TT_KEYWORD, 'and'), (Lexer.TT_KEYWORD, 'or'))))

        if res.erro:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini,
                self.token_atual.pos_fim,
                "Espera-se 'VAR, int, hex, id, '+', '-' or '('"
            ))
        
        return res.sucesso(no)
    
    def atom(self):
        res = ParserResultado.ParserResultado()
        #res.registro_de_avanco()
        #self.avancar()
        if self.token_atual.tipo_token in (Lexer.TT_INT, Lexer.TT_HEXA):
            res.registro_de_avanco()
            self.avancar()
            return res.sucesso(NumeroDeNos.NumeroDeNos(self.token_atual))
        
        elif self.token_atual.tipo_token == Lexer.TT_ID:
            res.registro_de_avanco()
            self.avancar()
            return res.sucesso(NumeroDeNos.VarEntraNo(self.token_atual))
        
        elif self.token_atual.tipo_token == Lexer.TT_LPAREN:
            res.registro_de_avanco()
            self.avancar()
            expr = res.registro(self.parser_expr())
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
            """
        elif tok.E_igual(Lexer.TT_KEYWORD, 'IF'):
            if_expr = res.registro(self.if_expr())
            if res.erro: return res
            return res.sucesso(if_expr)
            

        elif tok.E_igual(Lexer.TT_KEYWORD, 'print'):
            printp = res.registro(self.parser_print())
            if res.erro: return res
            return res.sucesso(printp)
            """
        return res.falha(Erro.SintaxeInvalidaErro(
            self.token_atual.pos_ini, self.token_atual.pos_fim,
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
        return self.bin_op(self.termo, ( Lexer.TT_PLUS, Lexer.TT_MINUS))
    
    def comp_expr(self):
        res = ParserResultado.ParserResultado()
        #Apagar esses res e self
        #res.registro_de_avanco()
        #self.avancar()
        print("Entrei no comp_expr")
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
    
        # Atualize a função `parse_cmds` no módulo Parser.py

    def parser_cmds(self):
        res = ParserResultado.ParserResultado()
        cmds = []
        
        """
        if tok.tipo_token != Lexer.TT_LBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro(
                tok.pos_ini, tok.pos_fim,
                "Espera-se abre chaves"
            ))
        """
        res.registro_de_avanco()
        self.avancar()

        """
        while tok.tipo_token in ((Lexer.TT_KEYWORD, 'print'),
                                 (Lexer.TT_KEYWORD, 'var'),
                                 Lexer.TT_ID,
                                 (Lexer.TT_KEYWORD, 'if'),
                                 (Lexer.TT_KEYWORD, 'while')):
        """
        if self.token_atual.tipo_token == Lexer.TT_EOF:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
            "Fim do arquivo sem fecha chaves"
            ))
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'print'):
            #res.registro_de_avanco()
            #self.avancar()
            res.registro(self.parser_print())
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'var'):
            res.registro(self.var())
        elif self.token_atual.tipo_token == Lexer.TT_ID:
            res.registro(self.parser_atribuicao())
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'if'):
            res.registro(self.parser_if())
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'while'):
            res.registro(self.parser_while())
        else:
            return res

        if res.erro: return res

        cmds.append(res.no)

        return res.sucesso(NumeroDeNos.BlocoNo(cmds, 
                                               self.token_atual.pos_ini, 
                                               self.token_atual.pos_fim))

    #Cmd -> print Exp ';'
    def parser_print(self):
        res = ParserResultado.ParserResultado()
        #res.registro_de_avanco()
        #self.avancar()

        exp = res.registro(self.parser_expr())
        if res.erro: return res

        res.registro_de_avanco()
        self.avancar()

        if self.token_atual.tipo_token != Lexer.TT_SEMICOLON:                
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini,
                self.token_atual.pos_fim,
                "Espera-se print"
            ))
        
        return res.sucesso(NumeroDeNos.PrintNo(
                                exp))
        

    #Cmd -> var NOME '=' Exp ';'   # declaração
    def var(self):
        res = ParserResultado.ParserResultado()
    

        if self.token_atual.tipo_token != Lexer.TT_ID:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "Espera-se 'Identificador'"))

        
        res.registro_de_avanco()
        self.avancar()
        
        if self.token_atual.tipo_token != Lexer.TT_EQ:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, 
                    self.token_atual.pos_fim,
                    "Espera-se '='"
                ))
        
        res.registro_de_avanco()
        self.avancar()
        expr = res.registro(self.parser_expr())
        if res.erro: return res

        res.registro_de_avanco()
        self.avancar()

        if not self.token_atual.tipo_token != Lexer.TT_SEMICOLON:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "Espera-se ';'"))

        return res.sucesso(NumeroDeNos.VarAlocadoNo(
            self.token_atual, expr))
        
        if res.erro:
            return res.falha(Erro.SintaxeInvalidaErro(
                tok.pos_ini,
                tok.pos_fim,
                "Espera-se var ID = EXP ;"
            ))
    #Bloco -> '{' Cmds '}'
    def parser_bloco(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual.tipo_token != Lexer.TT_LBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro
                             (self.token_atual.pos_ini, 
                              self.token_atual.pos_fim, 
                              "Bloco de comandos esperado (chave aberta '{')"))

        self.avancar()

        # Faz o parsing da sequência de comandos dentro do bloco
        cmds = []
        while self.token_atual.tipo_token != Lexer.TT_RBLOCO:
            cmd = res.registro(self.parser_cmds())
            if res.erro:
                return res
            cmds.append(cmd)


        # Verifica se o token atual é a chave fechada '}'
        if self.token_atual.tipo_token != Lexer.TT_RBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro
                             (self.token_atual.pos_ini, 
                              self.token_atual.pos_fim, 
                              "Bloco de comandos esperado (chave fechada '}')"))

        # Avança para o próximo token após a chave fechada
        self.avancar()

        # Retorna o nó representando o bloco de comandos
        return res.sucesso(NumeroDeNos.BlocoNo(cmds, 
                                   self.token_atual.pos_ini, 
                                   self.token_atual.pos_fim))

    #Cmd -> if Exp Bloco Elses
    def parser_if(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual.E_igual(Lexer.TT_KEYWORD, 'if'):
            res.registro_de_avanco()
            self.avancar()

            condicao = res.registro(self.parser_expr())
            if res.erro: return res

            bloco = res.registro(self.parser_bloco())
            if res.erro: return res
    
            elses = res.registro(self.parser_elses())
            if res.erro: return res

            return res.sucesso(NumeroDeNos.IfNo(condicao, 
                                                bloco, elses))
        
        
        return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
                f"Espera-se 'IF'"
                ))
    """
    Exp -> NUMERO
    Exp -> NOME
    Exp -> '(' Exp ')'
    Exp -> FunCall
    Exp -> UNOP Exp
    Exp -> Exp BINOP Exp
    """
    def parser_expr(self):
        res = ParserResultado.ParserResultado()
        #res.registro_de_avanco()
        #self.avancar()
        """
        if tok.tipo_token in (Lexer.TT_INT, Lexer.TT_HEXA):
            res.registro_de_avanco()
            self.avancar()
            expr = res.registro(self.parser_expr())
            if res.erro: return res
            return res.sucesso(expr)
            #return res.sucesso(NumeroDeNos.NumeroDeNos(tok))
        """
        no = res.registro(self.bin_op(self.comp_expr, (
            (Lexer.TT_KEYWORD, 'AND'), (Lexer.TT_KEYWORD, 'OR'))))

        if res.erro:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini,
                self.token_atual.pos_fim,
                "Espera-se Expressão"
            ))
        
        return res.sucesso(no)
    
    """
    Elses ->
    Elses -> else Bloco
    Elses -> elif Exp Bloco Elses
    """
    def parser_elses(self):
        res = ParserResultado.ParserResultado()

        if self.token_atual == None:
            return None

        elif not self.token_atual.E_igual(Lexer.TT_KEYWORD, 'else'):
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
                f"Espera-se 'ELSE'"
            ))
        res.registro_de_avanco()
        self.avancar()

        elifs = res.registro(self.parser_elif())
        if res.erro: return res

        bloco = res.registro(self.parser_bloco())
        if res.erro: return res

        elses = res.registro(self.parser_elses())
        if res.erro: return res

        return res.sucesso(NumeroDeNos.ElseNo(bloco, elses ))
    
    #Elses -> elif Exp Bloco Elses
    def parser_elif(self):
        res = ParserResultado.ParserResultado()

        if not self.token_atual.E_igual(Lexer.TT_KEYWORD, 'elif'):
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
                f"Espera-se 'ELIF'"
            ))
        res.registro_de_avanco()
        self.avancar()

        # Parse da expressão condicional
        exp_condicional = res.registro(self.parser_expr())
        if res.erro:return res

        bloco = res.registro(self.parser_bloco())
        if res.erro:return res

        elses = res.registro(self.parser_elses())
        if res.erro:return res

        return res.sucesso(NumeroDeNos.ElseNo(exp_condicional, bloco))

    #Cmd -> NOME '=' Exp;          # atribuição
    def parser_atribuicao(self):
        res = ParserResultado.ParserResultado()
        
        if self.token_atual == Lexer.TT_ID:
            res.registro_de_avanco()
            self.avancar()

            if self.token_atual.tipo_token != Lexer.TT_EQ:
                    return res.falha(Erro.SintaxeInvalidaErro(
                        self.token_atual.pos_ini, 
                        self.token_atual.pos_fim,
                        "Espera-se '='"
                    ))
            
            res.registro_de_avanco()
            self.avancar()
            expr = res.registro(self.parser_expr())
            if res.erro: return res

            if not self.token_atual.tipo_token != Lexer.TT_SEMICOLON:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, 
                    self.token_atual.pos_fim, 
                    "Espera-se ';'"))

            return res.sucesso(NumeroDeNos.VarAlocadoNo(
                self.token_atual, expr ))
        
        return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini,
                self.token_atual.pos_fim,
                "Espera-se ID = EXP ;"
            ))
    #Cmd -> while Exp Bloco
    def parser_while(self):
        res = ParserResultado.ParserResultado()
        
        if self.token_atual.E_igual(Lexer.KEYWORD, 'while'):
        
            exp = res.registro(self.parser_expr())
            if res.erro: return res

            bloco = res.registro(self.parser_bloco())
            if res.erro:return res
        
            return res.sucesso(NumeroDeNos.WhileNo(
                exp, bloco))
        
        return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini,
                self.token_atual.pos_fim,
                "Espera-se while Exp Bloco"
            ))
    
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