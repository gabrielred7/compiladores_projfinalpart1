/*
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_PROGRAM_SIZE 1000
#define MAX_STACK_SIZE 1000
#define MAX_LABELS 200

typedef enum {
    EXIT,
    NUMBER,
    ADD, SUB, MUL, DIV, POW,
    NOT, NEG,
    EQ, NEQ, LE, LEQ, GE, GEQ,
    LOAD, STORE,
    POP, DUP,
    PRINT,
    JUMP, JUMP_TRUE, JUMP_FALSE
} OpCode;

typedef struct {
    OpCode op;
    int valor;
} Instruction;

typedef struct {
    char label[4];
    int endereco;
} Label;

Label labels[MAX_LABELS];
int numLabels = 0;

void adicionarLabel(const char* label, int endereco) {
    Label novoLabel;
    strcpy(novoLabel.label, label); // esse metodo copia a string apontada pela origem para o destino.
    novoLabel.endereco = endereco;
    labels[numLabels++] = novoLabel;
}

int encontrarLabel(const char* label) {
    for (int i = 0; i < numLabels; i++) {
        if (strcmp(labels[i].label, label) == 0) {
            return labels[i].endereco;
        }
    }
    return -1; // Label nao encontrado
}

void assembler(const char* arquivo, Instruction* program, int* tamanhoPrograma) {
    //abri o arquivo
    FILE* file = fopen(arquivo, "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo. \n"); exit(1);
    }

    char linha[MAX_LABELS];
    int endereco = 0;

    while (fgets(linha, sizeof(linha), file)) {
        char* token = strtok(linha, " \t\n"); // esse metodo dividi string um por um:

        if (token == NULL) { continue; } // linha vazia
        
        // Primeiro, verifica se é um label
        if (token[strlen(token) - 1] == ':') {
            token[strlen(token) - 1] = '\0'; // Remove o ":" do final
            adicionarLabel(token, endereco);
            token = strtok(NULL, " \t\n");
            if (token == NULL) {
                continue; 
            }
        }

        // Monta a instrução referente ao token
        Instruction instrucao;
        if (strcmp(token, "EXIT") == 0) {
            instrucao.op = EXIT;
        } else if (strcmp(token, "NUMBER") == 0) { instrucao.op = NUMBER;
            token = strtok(NULL, " \t\n");
            if (!token) { printf("Valor ausente para NUMBER\n"); exit(1);
            } instrucao.valor = atoi(token);
        } else if (strcmp(token, "ADD") == 0) { instrucao.op = ADD;
        } else if (strcmp(token, "SUB") == 0) { instrucao.op = SUB;
        } else if (strcmp(token, "MUL") == 0) { instrucao.op = MUL;
        } else if (strcmp(token, "DIV") == 0) { instrucao.op = DIV;
        } else if (strcmp(token, "POW") == 0) { instrucao.op = POW;
        } else if (strcmp(token, "NOT") == 0) { instrucao.op = NOT;
        } else if (strcmp(token, "NEG") == 0) { instrucao.op = NEG;
        } else if (strcmp(token, "EQ") == 0) { instrucao.op = EQ;
        } else if (strcmp(token, "NEQ") == 0) { instrucao.op = NEQ;
        } else if (strcmp(token, "LE") == 0) { instrucao.op = LE;
        } else if (strcmp(token, "LEQ") == 0) { instrucao.op = LEQ;
        } else if (strcmp(token, "GE") == 0) { instrucao.op = GE;
        } else if (strcmp(token, "GEQ") == 0) { instrucao.op = GEQ;
        } else if (strcmp(token, "LOAD") == 0) { instrucao.op = LOAD;
            token = strtok(NULL, " \t\n");
            if (token == NULL) { printf("Valor ausente para LOAD\n"); exit(1);
            } instrucao.valor = atoi(token);
        } else if (strcmp(token, "STORE") == 0) { instrucao.op = STORE;
            token = strtok(NULL, " \t\n");
            if (token == NULL) { printf("Valor ausente para STORE\n"); exit(1);
            } instrucao.valor = atoi(token);
        } else if (strcmp(token, "POP") == 0) { instrucao.op = POP;
        } else if (strcmp(token, "DUP") == 0) { instrucao.op = DUP;
        } else if (strcmp(token, "PRINT") == 0) { instrucao.op = PRINT;
        } else if (strcmp(token, "JUMP") == 0) { instrucao.op = JUMP;
            token = strtok(NULL, " \t\n");
            if (token == NULL) { printf("Valor ausente para JUMP\n"); exit(1);
            } instrucao.valor = encontrarLabel(token) - endereco - 2; //Calcula o deslocamento relativo
        } else if (strcmp(token, "JUMP_TRUE") == 0) { instrucao.op = JUMP_TRUE;
            token = strtok(NULL, " \t\n");
            if (token == NULL) { printf("Valor ausente para JUMP_TRUE\n"); exit(1);
            } instrucao.valor = encontrarLabel(token) - endereco - 2; 
        } else if (strcmp(token, "JUMP_FALSE") == 0) {
            instrucao.op = JUMP_FALSE;
            token = strtok(NULL, " \t\n");
            if (token == NULL) { printf("Valor ausente para JUMP_FALSE\n"); exit(1);
            } instrucao.valor = encontrarLabel(token) - endereco - 2; 
        } else {
            printf("Unknown instruction: %s\n", token); exit(1);
        }
        program[endereco++] = instrucao;
    }

    fclose(file);
    *tamanhoPrograma = endereco;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <arquivo>\n", argv[0]);
        return 1;
    }

    Instruction program[MAX_PROGRAM_SIZE];
    int tamanhoPrograma;

    // Monta o bytecode a partir do arquivo de entrada
    assembler(argv[1], program, &tamanhoPrograma);

    return 0;
}