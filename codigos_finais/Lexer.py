"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

import Token
import Posicao
import Erro
import string

#CONSTANTES
DIGITOS = '0123456789'
HEXA    = '0123456789ABCDEF'
LETRAS  = string.ascii_letters #Todas as letras
LETRAS_DIGITOS = LETRAS + DIGITOS

#TOKENS

TT_INT		  = 'TokNumber'
TT_PLUS       = 'TokOp OpSum'
TT_MINUS      = 'TokOp OpSub'
TT_MUL        = 'TokOp OpMul'
TT_DIV        = 'TokOp OpDiv'
TT_MOD        = 'TokOp OpMod'
TT_EXP        = 'TokOp OpExp'
TT_LPAREN     = 'LPAREN'
TT_RPAREN     = 'RPAREN'
TT_COM1       = 'TokComment1'
TT_COM2       = 'TokComment2'
TT_ERRO       = 'TokError'
TT_HEXA       = 'TokHexadecimal'
TT_EOF        = 'EOF'
TT_KEYWORD    = 'Tok_KeyWord'
TT_ID         = 'Tok_ID'
TT_EQ         = 'Tok_EQ'
TT_2EQ        = 'Tok_2EQ'
TT_NEQ        = 'Tok_NEQ'
TT_MENORQUE   = 'Tok_MenorQue'
TT_MAIORQUE   = 'Tok_MaiorQue'
TT_MENOREQQUE = 'Tok_MenorEqQue'
TT_MAIOREQQUE = 'Tok_MaiorEqQue'
TT_LBLOCO     = 'LBLOCO'
TT_RBLOCO     = 'RBLOCO'
TT_SEMICOLON  = 'Tok_PontoEVirgula'
TT_COMMA      = 'Tok_Virgula'
TT_NEWLINE    = 'Tok_Nova_linha'


KEYWORD = [ 'var', 'and', 'or', 'not', 'if',
            'elif', 'else', 'print', 'while', 'fun']

#Classe que implementa o analisador léxico. 
class Lexer:
    def __init__(self, text):
        self.entrada = text
        self.posicao = Posicao.Posicao(-1, 0, -1, text)
        self.char_atual = None
        self.avancar()

    # O método avancar atribui a entrada ao char atual
    def avancar(self):
        self.posicao.avancar(self.char_atual)
        self.char_atual = self.entrada[self.posicao.idx] if self.posicao.idx < len(self.entrada) else None

    # Ignora espaços em branco (como space, tab e etc)
    def pular_espaco_branco(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()
    
    # Ignora caracteres de comentarios
    def pular_comentario_linha(self):
        while self.char_atual is not None and self.char_atual != '\n':
            self.avancar()
        self.avancar()
        return Token.Token(TT_COM1, pos_ini=self.posicao)
    # Ignora o que tá no comentário
    def pular_comentario_bloco(self):
        while self.char_atual is not None and self.char_atual !='\n':
                self.avancar()
                if self.char_atual == '*':
                    self.avancar()
                    if self.char_atual == '/':
                        return Token.Token(TT_COM2, pos_ini=self.posicao)
        self.avancar()

    def decimal(self):
        numero = ''
        pos_ini = self.posicao.copia()

        while self.char_atual is not None and self.char_atual in DIGITOS:
            numero += self.char_atual
            self.avancar()
        return Token.Token(TT_INT, int(numero),pos_ini, self.posicao)

    def letras(self):
        id = ''
        pos_ini = self.posicao.copia()

        while self.char_atual is not None and self.char_atual in LETRAS_DIGITOS + "_":
            id += self.char_atual
            self.avancar()
        tipo_token = TT_KEYWORD if id in KEYWORD else TT_ID
        return Token.Token(tipo_token, id, pos_ini, self.posicao)


    def hexadecimal(self):
        numero = ''
        pos_ini = self.posicao.copia()
        #while self.char_atual is not None and self.char_atual.isalnum():
        while self.char_atual is not None and self.char_atual in HEXA:
            numero += self.char_atual
            self.avancar()
        #if numero.startswith('0x'):
        return Token.Token(TT_HEXA, str(numero),pos_ini, self.posicao)

    def nao_Iguais(self):
        pos_ini = self.posicao.copia()
        self.avancar()

        if self.char_atual == '=':
            self.avancar()
            return Token.Token(TT_NEQ, pos_ini=pos_ini, pos_fim=self.posicao), None
        
        self.avancar()
        return None, Erro.CharEsperadoErro(pos_ini, self.posicao, "'=' depois de !")

    def Iguais(self):
        tipo_token = TT_EQ
        pos_ini = self.posicao.copia()
        self.avancar()

        if self.char_atual == '=':
            self.avancar()
            tipo_token = TT_2EQ

        return Token.Token(tipo_token, pos_ini=pos_ini, pos_fim=self.posicao)
    
    def menor_Que(self):
        tipo_token = TT_MENORQUE
        pos_ini = self.posicao.copia()
        self.avancar()

        if self.char_atual == '=':
            self.avancar()
            tipo_token = TT_MENOREQQUE

        return Token.Token(tipo_token, pos_ini=pos_ini, pos_fim=self.posicao)

    def maior_Que(self):
        tipo_token = TT_MAIORQUE
        pos_ini = self.posicao.copia()
        self.avancar()

        if self.char_atual == '=':
            self.avancar()
            tipo_token = TT_MAIOREQQUE

        return Token.Token(tipo_token, pos_ini=pos_ini, pos_fim=self.posicao)


    def operadores(self):
        op = self.char_atual
        if op == '+':
            return Token.Token(TT_PLUS, pos_ini=self.posicao)
        elif op == '-':
            return Token.Token(TT_MINUS, pos_ini=self.posicao)
        elif op == '*':
            return Token.Token(TT_MUL, pos_ini=self.posicao)
        elif op == '/':
            return Token.Token(TT_DIV, pos_ini=self.posicao)
        elif op == '%':
            return Token.Token(TT_MOD, pos_ini=self.posicao)
        elif op == '^':
            return Token.Token(TT_EXP, pos_ini=self.posicao)
        elif op == '=':
            return self.Iguais()
        elif op == '(':
            return Token.Token(TT_LPAREN, pos_ini=self.posicao)
        elif op == ')':
            return Token.Token(TT_RPAREN, pos_ini=self.posicao)
        elif op == '{':
            return Token.Token(TT_LBLOCO, pos_ini=self.posicao)
        elif op == '}':
            return Token.Token(TT_RBLOCO, pos_ini=self.posicao)
        elif op == ';':
            return Token.Token(TT_SEMICOLON, pos_ini=self.posicao)
        elif op == ',':
            return Token.Token(TT_COMMA, pos_ini=self.posicao)
        elif op == '<':
            return self.menor_Que()
        elif op == '>':
            return self.maior_Que()

    # Lê o caractere atual e retorna o proximo token
    def next(self):
        tokens = []

        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.avancar()

            elif self.char_atual == "\n":
                tokens.append(Token.Token(TT_NEWLINE, pos_ini=self.pos))
                self.avancar()

            elif self.char_atual in DIGITOS:
                tokens.append(self.decimal())

            elif self.char_atual in LETRAS:
                tokens.append(self.letras())

            elif self.char_atual == '!':
                token, erro = self.nao_Iguais()
                if erro: return [], erro
                tokens.append(token)

            elif self.char_atual in ('+', '-', '*', '/',
                                      '%', '^', '(',
                                      ')', '{', '}',';' 
                                      ,'=', '<', '>', ','):
                tokens.append(self.operadores())
                self.avancar()

            elif self.char_atual == '/':
                self.avancar()
                #if self.verificar() == '/':
                if self.char_atual == '/':
                    tokens.append(self.pular_comentario_linha())
                    self.avancar()
                #elif self.verificar() == '*':
                elif self.char_atual == '*':
                    tokens.append(self.pular_comentario_bloco())
                    self.avancar()
            elif self.char_atual == '0':
                numero = self.char_atual
                self.avancar()
                if self.char_atual == 'x':
                    self.avancar()
                    if self.char_atual in HEXA:
                        tokens.append(self.hexadecimal())
                else:
                    tokens.append(Token.Token(TT_INT, pos_ini=self.posicao))


            
            else:
                pos_erro = self.posicao.copia()
                char = self.char_atual
                self.avancar()
                return [TT_ERRO], Erro.CharIlegalErro(pos_erro, self.posicao,"'" + char + "'")

        tokens.append(Token.Token(TT_EOF, pos_ini=self.posicao))
        return tokens, None
