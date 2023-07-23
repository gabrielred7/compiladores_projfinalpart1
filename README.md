# **Trabalho final** 
## *compilador completo para a linguagem Arara*
Este compilador consiste de dois programas, o compilador Arara->Araque e a máquina virtual Araque.

## Integrantes do grupo:
- Gabriel Almeida Mendes - DRE: 117204959
- Marcus Vinicius Torres de Oliveira - DRE: 118142223

## Introdução:
Neste projeto, apresentamos um compilador completo para a linguagem Arara. O compilador é dividido em duas partes: o compilador Arara->Araque e a máquina virtual Araque.

A linguagem Arara é uma linguagem de programação simples que será compilada para a linguagem intermediária Araque, a qual será executada pela máquina virtual.

## Estrutura do Projeto:
O projeto está organizado da seguinte forma:

1. ### Analisador Léxico:
   A primeira etapa é a análise léxica. Ele lê o código-fonte Arara e o divide em uma  sequência de tokens (por exemplo, identificadores, números, operadores).
2. ### Análise Sintática (Parser):
   A secunda etapa é análise sintática, também conhecida como parser. O parser pega a sequência de tokens do scanner e constrói uma árvore de sintaxe abstrata (AST). O AST representa a estrutura hierárquica do código Arara com base nas regras gramaticais.
3. ### Geração de Código (Arara -> Araque)
   Essa etapa envolve percorrer o AST e gerar um código de texto correspondente do Araque.
4. ### Gerar o Bytecode Araque
   Essa etapa o arquivo de texto gerado é lido e o array de bytecodes é gerado.
5. ### Executa o programa
   Essa é a etapa final. Nela, a máquina virtual executa o programa e printa a saída na tela.

## Executando o codegenerator:
Para compilar o codegenerator:
1. 
```
python3 main.py
```
2. Cole o programa no terminal. OBS: Lá você pode botar algumas chamadas de funções, como por exemplo: fun printar(a){print a;} e ele retorna o bloco da função.
3. Gera o arquivo texto (programa.ara) com as instruções

## Executar o arac:
Para compilar o arac:
1. compila o arac
```
gcc -o arara arara.c
```
2. compilar o programa da linguagem Arara em bytecode Araque
```
./arara programa.ara > programa.arac
````

## Executar o aravm:
Para compilar o aravm:
1. compila o aravm
```
gcc -o aravm aravm.c
```
2. executa o programa Araque
```
./aravm programa.arac
```

## Problemas:
- Infelizmente não conseguimos trazer a AST para o compilador do parser python para o compilador em C.
- Utilizando um programa em Arara testamos o arac, jogamos o bytecode no aravm e tentamos executar. Infelizmente não obtivemos nada.
- Também tivemos dificuldades com a AST. A função if, else, elif, while e a chamada de função não estão parseando.

## Obs:
Ignorar os códigos do trabalho 3 do interpretador em python. O que importa é a classe lexer, parser e o numeroDeNos (sim, o nome é ruim, kkk) e os arquivos c.
