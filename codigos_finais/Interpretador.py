"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
import RTResultado
import Numero
import Lexer
import Erro

#Classe interpretador
class Interpretador:
    #Determina qual método chamar dependendo do tipo de nó.
    #Caso não ache, manda uma mensagem padrão.
    def visita(self, no, contexto):
        metodo_nome = f'visita_{type(no).__name__}'
        metodo = getattr(self, metodo_nome, self.metodo_nao_visitado)
        return metodo(no, contexto)
    
    #mensagem
    def metodo_nao_visitado(self, no, contexto):
        raise Exception(f'metodo visita_{type(no).__name__} não definido')
    
 ###########################################################
 # Metódos de visita para cada tipo de no   

    def visita_NumeroDeNos(self, no, contexto):
        return RTResultado.RTResultado().sucesso(
            Numero.Numero(no.tok.valor_token).set_contexto(contexto).set_pos(no.pos_ini, no.pos_fim)
        )
    
    
    def visita_VarEntraNo(self, no, contexto):
        res = RTResultado.RTResultado()
        var_nome = no.var_nome_token.valor_token
        valor = contexto.tabela_simbolo.get(var_nome)

        if not valor:
            return res.falha(Erro.RTErro(
                no.pos_ini, no.pos_fim,
                f"'{var_nome}' não está definida",
                contexto
            ))
        
        valor = valor.copia().set_pos(no.pos_ini, no.pos_fim)
        return res.sucesso(valor)
    
    
    def visita_VarAlocadoNo(self, no, contexto):
        res = RTResultado.RTResultado()
        var_nome = no.var_nome_token.valor_token
        valor = res.registro(self.visita(no.valor_no, contexto))
        if res.erro: return res

        contexto.tabela_simbolo.set(var_nome, valor)
        return res.sucesso(valor)

    def visita_BinOpNo(self, no, contexto):
        res = RTResultado.RTResultado()
        esq = res.registro(self.visita(no.no_esq, contexto))
        if res.erro: return res
        dir = res.registro(self.visita(no.no_dir, contexto))
        if res.erro: return res

        #erro = None
        #resultado = None
        if no.op_tok.tipo_token == Lexer.TT_PLUS:
            resultado, erro = esq.somado(dir)
        elif no.op_tok.tipo_token == Lexer.TT_MINUS:
            resultado, erro = esq.subtraido(dir)
        elif no.op_tok.tipo_token == Lexer.TT_MUL:
            resultado, erro = esq.multiplicado(dir)
        elif no.op_tok.tipo_token == Lexer.TT_DIV:
            resultado, erro = esq.dividido(dir)
        elif no.op_tok.tipo_token == Lexer.TT_EXP:
            resultado, erro = esq.exponenciado(dir)
        elif no.op_tok.tipo_token == Lexer.TT_2EQ:
            resultado, erro = esq.get_comparado_Eq(dir)
        elif no.op_tok.tipo_token == Lexer.TT_NEQ:
            resultado, erro = esq.get_comparado_Neq(dir)
        elif no.op_tok.tipo_token == Lexer.TT_MENORQUE:
            resultado, erro = esq.get_comparado_MenorQue(dir)
        elif no.op_tok.tipo_token == Lexer.TT_MAIORQUE:
            resultado, erro = esq.get_comparado_MaiorQue(dir)
        elif no.op_tok.tipo_token == Lexer.TT_MENOREQQUE:
            resultado, erro = esq.get_comparado_MenorEqQue(dir)
        elif no.op_tok.tipo_token == Lexer.TT_MAIOREQQUE:
            resultado, erro = esq.get_comparado_MaiorEqQue(dir)
        elif no.op_tok.E_igual(Lexer.TT_KEYWORD, "AND"):
            resultado, erro = esq.E(dir)
        elif no.op_tok.E_igual(Lexer.TT_KEYWORD, "OR"):
            resultado, erro = esq.Ou(dir)

        if erro:
            return res.falha(erro)
        else:
            return res.sucesso(resultado.set_pos(no.pos_ini, no.pos_fim))
        
    def visita_UnaryOpNo(self, no, contexto):
        res = RTResultado.RTResultado()
        numero = res.registro(self.visita(no.no, contexto))
        if res.erro: return res 

        erro = None

        if no.op_tok.tipo_token == Lexer.TT_MINUS:
            numero, erro = numero.multiplicado(Numero.Numero(-1))
        elif no.op_tok.E_igual(Lexer.TT_KEYWORD, 'NOT'):
            numero, erro = numero.Nao()

        if erro:
            return res.falha(erro)
        else:
            return res.sucesso(numero.set_pos(no.pos_ini, no.pos_fim))

    def visit_IfNo(self, no, contexto):
        res = RTResultado.RTResultado()

        for condicao, expr in no.cases:
            condicao_valor = res.registro(self.visita(condicao, contexto))
            if res.erro: return res

            if condicao_valor.is_true():
                expr_valor = res.registro(self.visita(expr, contexto))
                if res.erro: return res
                return res.sucesso(expr_valor)
            
        if no.else_case:
            else_valor = res.registro(self.visita(no.else_case, contexto))
            if res.erro: return res
            return res.sucesso(else_valor)
        
        return res.sucesso(None)
    
    def visita_BlocoNo(self, no, contexto):
        res = RTResultado.RTResultado()
        resultado = None

        for cmd in no.cmds:
            resultado = res.registro(self.visita(cmd, contexto))
            if res.erro:
                return res

        return res.sucesso(resultado)