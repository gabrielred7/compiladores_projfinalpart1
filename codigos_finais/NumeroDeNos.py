"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

############################################################
############################################################
#
#              CLASS DE NÓS
#
# Ela representa os nós para construir a árvore para a 
# linguagem Arara. 
############################################################
############################################################

"""
Essa classe representa um nó de um número (int ou hexa)
"""
class NumeroDeNos:
    def __init__(self, tok):
        self.tok = tok

        #Acessando a pos do no
        self.pos_ini = self.tok.pos_ini
        self.pos_fim = self.tok.pos_fim
    
    def __repr__(self):
        return f'{self.tok}'
    
"""
Essa classe representa um nó para operadores binários.
Com dois nós filhos da expressão da esquerda e da direita
do operador.
"""
class BinOpNo:
    def __init__(self, no_esq, op_tok, no_dir):
        self.no_esq = no_esq
        self.op_tok = op_tok
        self.no_dir = no_dir
        #Acessando a pos do no
        self.pos_ini = self.no_esq.pos_ini
        self.pos_fim = self.no_dir.pos_fim

    def __repr__(self):
        return f'({self.no_esq}, {self.op_tok}, {self.no_dir})'

"""
Essa classe representa um nó da árvore que contém um operador
unário, com um nó filho da expressão do operador.
"""
class UnaryOpNo:
    def __init__(self, op_tok, no):
        self.op_tok = op_tok
        self.no = no
        #Acessando a pos do no
        self.pos_ini = self.op_tok.pos_ini
        self.pos_fim = self.op_tok.pos_fim

    def __repr__(self):
        return f'({self.op_tok}, {self.no})'
    
"""
Essa classe representa um nó identificador 
(nome de variável).
"""
class VarEntraNo:
    def __init__(self, var_nome_token):
        self.var_nome_token = var_nome_token
        #Acessando a pos do no
        self.pos_ini = self.var_nome_token.pos_ini
        self.pos_fim = self.var_nome_token.pos_fim

"""
Essa classe representa um nó identificador(nome de var)
e o nó expressão que atribui valor a variável.
"""
class VarAlocadoNo:
    def __init__(self, var_nome_token, valor_no):
        self.var_nome_token = var_nome_token
        self.valor_no = valor_no
        #Acessando a pos do no
        self.pos_ini = self.var_nome_token.pos_ini
        self.pos_fim = self.valor_no.pos_fim


"""
Essa classe representa um nó 'if'.
Contém a condição, o bloco de comandos do 'if' e,
opcionalmente, um bloco 'else'.
"""
class IfNo:
    
    def __init__(self, condicao, bloco, elses=None):
        self.condicao = condicao
        self.bloco = bloco
        self.elses = elses

    def __repr__(self):
        return f'if {self.exp} {self.bloco} {self.elses}'
        

"""
Essa classe representa um nó bloco de comandos.
Contém uma lista de nós dos comandos.
"""
class BlocoNo:
    def __init__(self, comandos):
        self.comandos = comandos

    def __repr__(self):
        cmds_str = '\n'.join(str(cmd) for cmd in self.comandos)
        return f'{{\n{cmds_str}\n}}'

"""
Essa classe representa um nó else e uma estrutura opicional.
Contém aexpressão condicional e o bloco de comandos associado.
"""
class ElseNo:
    def __init__(self, exp_condicional, bloco):
        self.exp_condicional = exp_condicional
        self.bloco = bloco

"""
Essa classe representa um nó print. Contém a expressão 
cujo valor será impresso na tela.
"""
class PrintNo:
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return f'print {self.exp}'

"""
Essa classe representa um nó while. Contém a expressão
que determina a condição do laço e o bloco de comandos
associado.
"""
class WhileNo:
    def __init__(self, exp, bloco):
        self.exp = exp
        self.bloco = bloco

    def __repr__(self):
        return f'while {self.exp} {self.bloco}'
    
"""
Essa classe representa um nó para função. Contém o nome da 
função, seus argumentos, o corpo da função e o contexto
(ambiente de execução) associado.
"""
class FuncNo:
    def __init__(self, nome, args, corpo, contexto):
        self.nome = nome  
        self.args = args  
        self.corpo = corpo  
        self.contexto = contexto  

    def __repr__(self):
        args_str = ', '.join(str(arg.valor_token) for arg in self.args)
        return f"FuncNo(nome={self.nome.valor_token}, args=[{args_str}], corpo={self.corpo}, contexto={self.contexto})"

"""
Essa classe representa um nó para definição de função.
Contém o token do nome da função, uma lista de tokens 
dos nomes dos argumentos e o nó do corpo da função.
"""
class FuncDefNo:
    def __init__(self, var_nome_tok, arg_nome_toks, corpo_no):
        self.var_nome_tok = var_nome_tok
        self.arg_nome_toks = arg_nome_toks
        self.corpo_no = corpo_no
        
"""
Essa classe representa um nó chamada de função. Contém o nó da 
função a ser chamada e a lista de nós representando os argumentos
da chamada.
"""
class FunCallNo:
    def __init__(self, no_para_chamar, no_args):
        self.no_para_chamar = no_para_chamar
        self.no_args = no_args

"""
Essa classe representa um nó para o comando de atribuição.
Contém o nó do identificador da variável e o nó da expressão
que atribui valor à variável.
"""
class AtribuicaoNo:
    def __init__(self, var_nome, exp):
        self.var_nome = var_nome
        self.exp = exp

    def __repr__(self):
        return f'{self.var_nome} = {self.exp};'
    
"""
Essa classe representa um nó  para o comando de 
declaração de variável. Contém o nó do identificador 
da variável e o nó da expressão que inicializa a variável.
"""
class DeclaracaoNo:
    def __init__(self, var_nome, exp):
        self.var_nome = var_nome
        self.exp = exp

    def __repr__(self):
        return f'var {self.var_nome} = {self.exp};'

"""
Essa classe representa uma lista de nós de função definidos
no código fonte. Ela armazena os nós de todas as funções
definidas no programa.
"""
class ListaDeFuncoes:
    def __init__(self):
        self.funcoes = []

    def adicionar_funcao(self, func):
        self.funcoes.append(func)

    def get_funcoes(self):
        return self.funcoes

    def __repr__(self):
        return f"ListaDeFuncoes({self.funcoes})"
