"""
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
"""

gramatica:   
Expressão: E  
    E -> num
    E -> ( E )
    E -> + E E
    E -> - E E
    E -> * E E
    E -> / E E
    E -> ^ E E

Se você conseguir, implemente expressões infixadas,
com o operador entre as expressões. A^B, (A+B)*C, etc.
   * Os operadores + - * / devem ser associativos à esquerda
   * O operador ^, de exponenciação, deve ser associativo à direita
   * Os níveis de precedência devem ser:

        1. ^        
        2. * e /
        3. + e -

expr  : KEYWORD:VAR ID EQ expr
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
      : if-expr

CMDS:
if-expr : KEYWORD: IF expr { CMDS }
         KEYWORD: ELIF expr { CMDS }*
         KEYWORD: ELSE { CMDS}?