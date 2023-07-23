"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

#Imports
import Lexer
import ParserResultado
import NumeroDeNos
import Erro


##########################################################
##########################################################
#
# PARSER
#
##########################################################
##########################################################

#Classe que implementa o parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.avancar()
    # Avança para o próximo token e atualiza o token atual
    def avancar(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.token_atual = self.tokens[self.tok_idx]
        return self.token_atual
    
    """
    O método parser_programa é o método que inicia a analise 
    sintática do programa. Ele chama o método parser_funcs()
    para analisar a definição das funções do programa.
    Se tudo estiver certo, ele retornar a AST
    """
    # Regra principal da gramática: Programa -> Funcs
    def parser_programa(self):
        res = self.parser_funcs()
        # Verifica se não ocorreu alguma falha
        if not res.erro and self.token_atual.tipo_token != Lexer.TT_EOF:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim, 
                "Ocorreu alguma falha" 
            ))
        return res


##########################################################
##########################################################
#
# METODOS DAS REGRAS DA GRAMÁTICA
#
#Esses são os métodos do analisador sintático. Eles são
#responsáveis por criar a árvore.  
##########################################################
##########################################################
"""
    # Lista de funções (zero ou mais, sem separador)
    #Funcs -> {FuncDef}

    Esse método analisa a lista de funções no programa. Ele
    le os tokens até encontrar uma chamada de função. Ai 
    chama o método parser_funcdef() para analisar a função.
    Ele fica no loop até achar o final do arquivo. No final
    ele retorna a lista com cada função.
"""
    def parser_funcs(self):
        res = ParserResultado.ParserResultado()
        funcs = []
        
        while self.token_atual.tipo_token != Lexer.TT_EOF:
            # Verifica se o token atual = fun
            if self.token_atual.E_igual(Lexer.TT_KEYWORD, 'fun'):
                # Chama o parser para a função
                funcs.append(res.registro(self.parser_funcdef()))
                if res.erro:
                    return res.falha(Erro.SintaxeInvalidaErro(
                        self.token_atual.pos_ini,
                        self.token_atual.pos_fim,
                        "Ocorreu algum erro com as funções"
                    ))
            
                
            else:
                # Se o token atual != fun ,
                # erro de sintaxe
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini,
                    self.token_atual.pos_fim,
                    "Espera-se palavra-chave 'fun'"
                ))
            
        return res.sucesso(funcs)
        
    """
    Regra:
    #FuncDef -> 'fun' NOME '(' Args ')' Bloco
    #Só entra nessa função se o token atual for 'fun'

    Esse método analisa a regra da função. Retorna um nó de
    função. 
    """
    def parser_funcdef(self):
        
        res = ParserResultado.ParserResultado()
        arg_nomes_toks = []
        cmds_do_bloco = []
        #Avança
        res.registro_de_avanco()
        self.avancar()
        #Vê se o token atual é um ID (NOME)
        if  self.token_atual.tipo_token != Lexer.TT_ID:
            return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, 
                    self.token_atual.pos_fim, 
                    "Espera-se um NOME"))


        if self.token_atual.tipo_token == Lexer.TT_ID:         
            nome_func = self.token_atual
            res.registro_de_avanco()
            self.avancar()
            if self.token_atual.tipo_token != Lexer.TT_LPAREN:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, 
                    self.token_atual.pos_fim, 
                    "'(' esperado"))

            res.registro_de_avanco()
            self.avancar()

            if self.token_atual == Lexer.TT_RPAREN:
                arg_nomes_toks = None
                res.registro_de_avanco()
                self.avancar()
            else:
                
                arg_nomes_toks = self.parser_args()
                if arg_nomes_toks.erro:return arg_nomes_toks
                
                
        
        if self.token_atual.tipo_token != Lexer.TT_RPAREN:
                return res.falha(Erro.SintaxeInvalidaErro(
                    self.token_atual.pos_ini, 
                    self.token_atual.pos_fim, 
                    "')' esperado"))
        
        
        res.registro_de_avanco()
        self.avancar()
        

        cmds_do_bloco = self.parser_bloco()
        if cmds_do_bloco.erro:return cmds_do_bloco
        

        return res.sucesso(NumeroDeNos.FuncDefNo(
            nome_func, 
            arg_nomes_toks, cmds_do_bloco.no))

    """
    Regra:
     # Lista de nomes (zero ou mais, separado por vírgula)
        Args -> 
        Args -> NOME {',' NOME}

    Esse método analisa uma lista de args e retorna uma lista
    contendo os tokens dos nomes do args.
    """
    def parser_args(self):
        res = ParserResultado.ParserResultado()
        args = []

        if self.token_atual.tipo_token == Lexer.TT_ID:
            
            args.append(self.token_atual)
            res.registro_de_avanco()
            self.avancar()

            while self.token_atual.tipo_token == Lexer.TT_COMMA:
                res.registro_de_avanco()
                self.avancar()
                
                if self.token_atual.tipo_token != Lexer.TT_ID:
                    return res.falha(Erro.SintaxeInvalidaErro(
                        self.token_atual.pos_ini, 
                        self.token_atual.pos_fim, 
                        f"Nome da variável esperado"))
                args.append(self.token_atual)
                res.registro_de_avanco()
                self.avancar()
           
        
        return res.sucesso(args)
    """
    #Bloco -> '{' Cmds '}'

    Este método analisa um bloco de comandos. Ele reconhece
    os cmds até o fechamento de chaves. Retorna uma lista 
    de nós dos comandos no bloco.
    """
    def parser_bloco(self):
        res = ParserResultado.ParserResultado()
        cmds = []
        
        if self.token_atual.tipo_token != Lexer.TT_LBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro
                             (self.token_atual.pos_ini, 
                              self.token_atual.pos_fim, 
                              "Bloco de comandos esperado (chave aberta '{')"))
        
        res.registro_de_avanco()
        self.avancar()
        if self.token_atual == Lexer.TT_RBLOCO:
            return res.sucesso(cmds)

        
        while self.token_atual.tipo_token != Lexer.TT_RBLOCO:
            cmd = res.registro(self.parser_cmds())
            if res.erro:
                return res
            cmds.append(cmd)
            res.registro_de_avanco()
            self.avancar()


        # Verifica se o token atual é a chave fechada '}'
        if self.token_atual.tipo_token != Lexer.TT_RBLOCO:
            return res.falha(Erro.SintaxeInvalidaErro
                             (self.token_atual.pos_ini, 
                              self.token_atual.pos_fim, 
                              "Bloco de comandos esperado (chave fechada '}')"))

        
        
        res.registro_de_avanco()
        self.avancar()
        
        
        return res.sucesso(cmds)
    
    """
    # Lista de expressões (zero ou mais, separadas por vírgula)
    Exps -> 
    Exps -> Exp {',' Exp} 

    Este método analisa uma lista de expressões. Retorna
    uma lista de nós de expressões.

    OBS: Método quebrado
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

##########################################################
##########################################################
#Os métodos fator, termo, atom, pot, expr_aritm, comp_expr
#são usados para construir as expressões aritméticas e 
#lógicas. Eles lidam com ops unários, binários, nums, etc.
#Eu reaprovetei eles do trabalho 3.
##########################################################
##########################################################
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

    
    
    def atom(self):
        res = ParserResultado.ParserResultado()
        
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
            
        return res.falha(Erro.SintaxeInvalidaErro(
            self.token_atual.pos_ini, self.token_atual.pos_fim,
            "Espera-se int, hexa, id, '+', '-', '('"
        ))
    

    def pot(self):
        return self.bin_op(self.atom, (Lexer.TT_EXP, ), self.fator)

    def expr_Aritm(self):
        return self.bin_op(self.termo, ( Lexer.TT_PLUS, Lexer.TT_MINUS))
    
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

############################################################
############################################################
    
    """"
    Cmd -> print Exp ';'
    Cmd -> var NOME '=' Exp ';'   # declaração
    Cmd -> NOME '=' Exp;          # atribuição
    Cmd -> while Exp Bloco
    Cmd -> if Exp Bloco Elses
    Cmd -> FunCall ';'

    Este método analisa os comandos. Reconhe o print, 
    atribuição, declaração, if e while.
    """   

    def parser_cmds(self):
        res = ParserResultado.ParserResultado()
        cmd = None
        
        if self.token_atual.tipo_token == Lexer.TT_EOF:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, self.token_atual.pos_fim,
            "Fim do arquivo sem fecha chaves"
            ))
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'print'):
            
            cmd = res.registro(self.parser_print())
            if res.erro: return res
            return res.sucesso(cmd)
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'var'):
            cmd = res.registro(self.var())
            if res.erro: return res
            return res.sucesso(cmd)
        elif self.token_atual.tipo_token == Lexer.TT_ID:
            res.registro_de_avanco()
            self.avancar()
            if self.token_atual.tipo_token == Lexer.TT_EQ:
                cmd = res.registro(self.parser_atribuicao())
                if res.erro: return res
                return res.sucesso(cmd)
            elif self.token_atual.tipo_token == Lexer.TT_LPAREN:
                cmd = res.registro(self.parser_call())
                if res.erro: return res
                return res.sucesso(cmd)
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'if'):
            res.registro(self.parser_if())
        elif self.token_atual.E_igual(Lexer.TT_KEYWORD, 'while'):
            cmd = res.registro(self.parser_while())
            if res.erro: return res
            return res.sucesso(cmd)
        
        else:
            return res

        if res.erro: return res


        return res.sucesso(cmd)

############################################################
############################################################
# Os métodos print, dec de variável, atribuição, if, else,
#elif e chamada de função (Call)
#
#OBS: IF, ELSE, ELIF, WHILE E CALL QUEBRADOS
############################################################
############################################################
    #Cmd -> print Exp ';'
    def parser_print(self):
        res = ParserResultado.ParserResultado()
        res.registro_de_avanco()
        self.avancar()
        

        exp = res.registro(self.parser_expr())
        if res.erro: return res
        
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
        res.registro_de_avanco()
        self.avancar()

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
        
    

        if self.token_atual.tipo_token != Lexer.TT_SEMICOLON:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "Espera-se ';'"))

        return res.sucesso(NumeroDeNos.VarAlocadoNo(
            self.token_atual, expr))
        

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
        res.registro_de_avanco()
        self.avancar()
        expr = res.registro(self.parser_expr())
        if res.erro: return res

        if self.token_atual.tipo_token != Lexer.TT_SEMICOLON:
            return res.falha(Erro.SintaxeInvalidaErro(
                self.token_atual.pos_ini, 
                self.token_atual.pos_fim, 
                "Espera-se ';'"))

        return res.sucesso(NumeroDeNos.VarAlocadoNo(
            self.token_atual, expr ))
        
    #Cmd -> while Exp Bloco
    def parser_while(self):
        res = ParserResultado.ParserResultado()
        res.registro_de_avanco()
        self.avancar()
        
        exp = res.registro(self.parser_expr())
        if res.erro: return res

        bloco = res.registro(self.parser_bloco())
        if res.erro:return res
        
        res.registro_de_avanco()
        self.avancar()
        
        return res.sucesso(NumeroDeNos.WhileNo(
            exp, bloco))
        

    #FunCall -> NOME '(' Exps ')'
    def parser_call(self):
        res = ParserResultado.ParserResultado()
        calls = []

        if self.token_atual.tipo_token == Lexer.TT_RPAREN:
            return res.sucesso(calls)
        
        calls.append(res.registro(self.parser_exps))

        if self.token_atual.tipo_token == Lexer.TT_RPAREN:
            return res.sucesso(calls)

############################################################
############################################################

"""
Este método é usado para as expressões binárias. 
"""
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
