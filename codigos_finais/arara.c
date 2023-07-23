/*
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include "arara_ast.h" // Suponha que o arquivo com as definições da AST seja "arara_ast.h"

typedef struct No {
    int tipo;
    int valor;
    struct No* esquerda;
    struct No* direita;
} No;

// Tipos de instruções da máquina virtual "Araque"
typedef enum {
    // Aritméticas
    ADD, // Soma
    SUB, // Subtração
    MUL, // Multiplicação
    DIV, // Divisão
    POW, // Potência

    // Comparação
    EQ,  // Igual a
    NEQ, // Diferente de
    LE,  // Menor que
    LEQ, // Menor ou igual a
    GE,  // Maior que
    GEQ, // Maior ou igual a

    // Controle de fluxo
    JUMP,      // Salto incondicional
    JUMP_TRUE, // Salto se verdadeiro
    JUMP_FALSE,// Salto se falso

    // Manipulação da pilha
    LOAD,  // Carrega valor da memória
    STORE, // Armazena valor na memória
    POP,   // Remove valor do topo da pilha
    DUP,   // Duplica o valor no topo da pilha

    // Entrada/saída
    PRINT, // Imprime valor na tela

    // Outras
    NUMBER // Número
} OpCode;

void gerar_bytecode(FILE* arquivo_saida, No* no) {
    if (no == NULL) {
        return;
    }

    switch (no->tipo) {
        case NUMBER:
            fprintf(arquivo_saida, "NUMBER %d\n", no->valor);
            break;
        case ADD:
            fprintf(arquivo_saida, "ADD\n");
            break;
        case SUB:
            fprintf(arquivo_saida, "SUB\n");
            break;
        case MUL:
            fprintf(arquivo_saida, "MUL\n");
            break;
        case DIV:
            fprintf(arquivo_saida, "DIV\n");
            break;
        case POW:
            fprintf(arquivo_saida, "POW\n");
            break;
        case EQ:
            fprintf(arquivo_saida, "EQ\n");
            break;
        case NEQ:
            fprintf(arquivo_saida, "NEQ\n");
            break;
        case LE:
            fprintf(arquivo_saida, "LE\n");
            break;
        case LEQ:
            fprintf(arquivo_saida, "LEQ\n");
            break;
        case GE:
            fprintf(arquivo_saida, "GE\n");
            break;
        case GEQ:
            fprintf(arquivo_saida, "GEQ\n");
            break;
        case JUMP:
            fprintf(arquivo_saida, "JUMP %d\n", no->valor);
            break;
        case JUMP_TRUE:
            fprintf(arquivo_saida, "JUMP_TRUE %d\n", no->valor);
            break;
        case JUMP_FALSE:
            fprintf(arquivo_saida, "JUMP_FALSE %d\n", no->valor);
            break;
        case LOAD:
            fprintf(arquivo_saida, "LOAD %d\n", no->valor);
            break;
        case STORE:
            fprintf(arquivo_saida, "STORE %d\n", no->valor);
            break;
        case POP:
            fprintf(arquivo_saida, "POP\n");
            break;
        case DUP:
            fprintf(arquivo_saida, "DUP\n");
            break;
        case PRINT:
            fprintf(arquivo_saida, "PRINT\n");
            break;
        default:
            break;
    }

    gerar_bytecode(arquivo_saida, no->esquerda);
    gerar_bytecode(arquivo_saida, no->direita);
}


void compilar_arara(FILE* arquivo_saida, No* programa) {
    gerar_bytecode(arquivo_saida, programa);
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Uso: %s <arquivo_entrada>\n", argv[0]);
        return 1;
    }

    char* arquivo_entrada = argv[1];
    char arquivo_saida[strlen(arquivo_entrada) + 2];
    strcpy(arquivo_saida, arquivo_entrada);
    strcat(arquivo_saida, "c"); // Adiciona o sufixo ".arac" ao nome do arquivo de saída

    // Abre o arquivo de entrada em modo de leitura
    FILE* arquivo = fopen(arquivo_entrada, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo de entrada: %s\n", arquivo_entrada);
        return 1;
    }

    // Realiza a análise léxica, sintática e constrói a AST
    No* programa = analisar_programa(arquivo);
    fclose(arquivo);

    if (programa == NULL) {
        printf("Erro na análise do arquivo de entrada: %s\n", arquivo_entrada);
        return 1;
    }

    // Abre o arquivo de saída em modo de escrita
    FILE* arquivo_saida = fopen(arquivo_saida, "w");
    if (arquivo_saida == NULL) {
        printf("Erro ao criar o arquivo de saída: %s\n", arquivo_saida);
        liberar_no(programa);
        return 1;
    }

    // Compila o programa para bytecode e escreve no arquivo de saída
    compilar_arara(arquivo_saida, programa);

    // Libera a memória alocada para a AST
    liberar_no(programa);

    // Fecha o arquivo de saída
    fclose(arquivo_saida);

    printf("Compilação concluída com sucesso. Arquivo .arac gerado: %s\n", arquivo_saida);

    return 0;
}
