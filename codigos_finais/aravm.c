/*
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
*/

/**********************************************************
 * ***************** Maquina Virtual **********************
 * 
 * Executa um bytecode gerado e printa
 * Obs: Quebrado
***********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_STACK_SIZE 1000
/**
 * Define as operações que a máquina executa.
*/
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

/**
 * Essa struct é usada para armazenar cada instrução do 
 * bytecode.
*/
typedef struct {
    OpCode op;
    int value;
} Instruction;

/**
 * Executa o bytecode. Ela recebe um ponteiro para o bytecode
 * e o tamanho do bytecode em número de elementos (inteiros) 
 * como parâmetros. 
 * 
 * A máquina virtual possui uma pilha para armazenar os valores 
 * durante a execução, um contador de programa que mantém o 
 * índice atual da instrução sendo executada e um índice que 
 * rastreia o topo da pilha. A função itera sobre as
 * instruções do bytecode usando um loop while e executa
 *  as operações apropriadas para cada instrução usando 
 * um switch-case.
*/

void run(const Instruction* bytecode, int size) {
    int stack[MAX_STACK_SIZE];
    int top = 0;
    int pc = 0;

    while (pc < size) {
        Instruction instruction = bytecode[pc++];

        switch (instruction.op) {
            case EXIT:
                return;
            case NUMBER:
                stack[top++] = instruction.value;
                break;
            case ADD:
                stack[top - 2] += stack[top - 1];
                top--;
                break;
            case SUB:
                stack[top - 2] -= stack[top - 1];
                top--;
                break;
            case MUL:
                stack[top - 2] *= stack[top - 1];
                top--;
                break;
            case DIV:
                stack[top - 2] /= stack[top - 1];
                top--;
                break;
            case POW:
                stack[top - 2] = (int)pow(stack[top - 2], stack[top - 1]);
                top--;
                break;
            case NOT:
                stack[top - 1] = !stack[top - 1];
                break;
            case NEG:
                stack[top - 1] = -stack[top - 1];
                break;
            case EQ:
                stack[top - 2] = stack[top - 2] == stack[top - 1];
                top--;
                break;
            case NEQ:
                stack[top - 2] = stack[top - 2] != stack[top - 1];
                top--;
                break;
            case LE:
                stack[top - 2] = stack[top - 2] < stack[top - 1];
                top--;
                break;
            case LEQ:
                stack[top - 2] = stack[top - 2] <= stack[top - 1];
                top--;
                break;
            case GE:
                stack[top - 2] = stack[top - 2] > stack[top - 1];
                top--;
                break;
            case GEQ:
                stack[top - 2] = stack[top - 2] >= stack[top - 1];
                top--;
                break;
            case LOAD:
                stack[top++] = stack[instruction.value];
                break;
            case STORE:
                stack[instruction.value] = stack[top - 1];
                top--;
                break;
            case POP:
                top--;
                break;
            case DUP:
                stack[top] = stack[top - 1];
                top++;
                break;
            case PRINT:
                printf("%d\n", stack[--top]);
                break;
            case JUMP:
                pc += instruction.value;
                break;
            case JUMP_TRUE:
                if (stack[--top])
                    pc += instruction.value;
                break;
            case JUMP_FALSE:
                if (!stack[--top])
                    pc += instruction.value;
                break;
            default:
                printf("Unknown instruction\n");
                exit(1);
        }
    }
}

/**
 * Main.  Ela verifica se o programa foi chamado 
 * com o número correto de argumentos (um arquivo de entrada)
 * e abre o arquivo em modo binário ("rb"). Em seguida,
 * ela lê o conteúdo do arquivo binário para o ponteiro
 * bytecode, aloca espaço na memória para o array bytecode 
 * e preenche o array lendo o conteúdo do arquivo. Depois
 * disso, ela chama a função run passando o bytecode e o 
 * tamanho para iniciar a execução da máquina virtual.
 * Finalmente, o espaço alocado para o bytecode é liberado 
 * com free e o programa é encerrado com status de sucesso.
*/

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <program.arac>\n", argv[0]);
        return 1;
    }

    FILE* file = fopen(argv[1], "rb");
    if (!file) {
        printf("Error opening file: %s\n", argv[1]);
        return 1;
    }

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);

    Instruction* bytecode = (Instruction*)malloc(size);
    fread(bytecode, sizeof(Instruction), size / sizeof(Instruction), file);
    fclose(file);

    run(bytecode, size / sizeof(Instruction));

    free(bytecode);
    return 0;
}
