"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""
import RTResultado
import Numero
import Lexer

#Classe interpretador
class Interpretador:
    def visita(self, no, contexto):
        metodo_nome = f'visita_{type(no).__name__}'
        metodo = getattr(self, metodo_nome, self.metodo_nao_visitado)
        return metodo(no, contexto)
    
    def metodo_nao_visitado(self, no, contexto):
        raise Exception(f'Nao visita_{type(no).__name__} metodo definido')
    
    def visita_NumeroDeNos(self, no, contexto):
        return RTResultado.RTResultado().sucesso(
            Numero.Numero(no.tok.valor_token).set_contexto(contexto).set_pos(no.pos_ini, no.pos_fim)
        )
    
    def visita_BinOpNo(self, no, contexto):
        res = RTResultado.RTResultado()
        esq = res.registro(self.visita(no.no_esq, contexto))
        if res.erro: return res
        dir = res.registro(self.visita(no.no_dir, contexto))
        if res.erro: return res

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

        if erro:
            return res.falha(erro)
        else:
            return res.sucesso(resultado.set_pos(no.pos_ini, no.pos_fim))
        
    def visita_UnaryOpNo(self, no, contexto):
        res = RTResultado.RTResultado()
        numero = res.registro(self.visita(no.no, contexto))
        if res.erro: return res 

        erro = None

        if no.op_tok.ttype == Lexer.TT_MINUS:
            numero, erro = numero.multiplicado(Numero.Numero(-1))

        if erro:
            return res.falha(erro)
        else:
            return res.sucesso(numero.set_pos(no.pos_ini, no.pos_fim))

