#Arquivo principal

import sys
import Lexer

def main():
    texto_entrada = sys.stdin.read()
    lexer = Lexer(texto_entrada)
    while True:
        token = lexer.next()
        if token.tipo_token == 'TokEOF':
            break #Fim dos arquivos
        print(token.tipo_token, token.valor_token)


if __name__ == '__main__':
    main()