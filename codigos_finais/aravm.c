/*
Nomes: Gabriel Almeida Mendes - DRE: 117204959
       Marcus Vinicius Torres de Oliveira - DRE: 118142223
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_STACK_SIZE 1000

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
    int value;
} Instruction;

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
