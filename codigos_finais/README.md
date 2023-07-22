"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""


#Gramática de Arara:
##Aproveitando parte do código e parte da gramática do trabalho 3   
Programa -> Funcs
   
    # Lista de funções (zero ou mais, sem separador)
    Funcs -> {FuncDef}
   
    # Lista de nomes (zero ou mais, separado por vírgula)
    Args -> 
    Args -> NOME {',' NOME}
   
    # Lista de expressões (zero ou mais, separadas por vírgula)
    Exps -> 
    Exps -> Exp {',' Exp} 
   
    # Lista de comandos (zero ou mais, sem separador)
    Cmds -> {Cmd}   
   
    # Função
    FuncDef -> 'fun' NOME '(' Args ')' Bloco
   
    # Comandos
    Bloco -> '{' Cmds '}'
    
    Cmd -> print Exp ';'
    Cmd -> var NOME '=' Exp ';'   # declaração
    Cmd -> NOME '=' Exp;          # atribuição
    Cmd -> while Exp Bloco
    Cmd -> if Exp Bloco Elses
    Cmd -> FunCall ';'
    
    Elses ->
    Elses -> else Bloco
    Elses -> elif Exp Bloco Elses

    Exp -> NUMERO
    Exp -> NOME
    Exp -> '(' Exp ')'
    Exp -> FunCall
    Exp -> UNOP Exp
    Exp -> Exp BINOP Exp
   
    FunCall -> NOME '(' Exps ')'

expr : 
        :comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*

comp-expr : NOT comp-expr
              :Expr-Aritm ((==|<|>|<=|>=) Expr-Aritm)*

Expr-Aritm  : termo ((SOMA|SUB) termo)*

termo : fator ((EXP|MULT|DIV) fator)*

fator : (SOMA|SUB) fator
            : pot


pot   : atom (pot fator)^

atom  :INT|HEX|ID
      :LPAREN expr RPAREN
      

Os operadores unários são:

   - Negação aritmética: '-'
   - Negação booleana: not

Os operadores binários são:

   * aritméticos: + - * / ^
   * comparações: == != < > <= >=
   * booleanos: and or
   
A precedência dos operadores deve ser:

   - or
   - and
   - comparações
   - soma e subtração
   - multiplicação e divisão
   - operadores unários (negação)
   - exponenciação

Todos os operadores binários devem ser associativos à esquerda, exceto a exponenciação que deve ser associativa à direita.
