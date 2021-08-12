#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 200 //The number digit limitation

typedef struct _btnode
{
    int item;
    struct _btnode *left;
    struct _btnode *right;
} BTNode; // You should not change the definition of BTNode

typedef struct _node
{
    BTNode *item;
    struct _node *next;
} StackNode;

typedef struct _stack
{
    int size;
    StackNode *head;
} Stack;

void deleteTree(BTNode **root);

char *createExpTree(BTNode **root, char *prefix);
void printTree(BTNode *node);
void printTreePostfix(BTNode *node);
double computeTree(BTNode *node);
int isOperator(char *);
int isOperatorInt(int);
double computeOperation(char, int, int);

void push(Stack *sPtr, BTNode *item);
int pop(Stack *sPtr);
BTNode *peek(Stack s);
int isEmptyStack(Stack s);

int main()
{
    char prefix[SIZE];
    BTNode *root = NULL;

    //printf("Enter an prefix expression:\n");
    gets(prefix);
    char *p = strtok(prefix, " ");
    createExpTree(&root, p);

    // printf("The Infix Expression:\n");
    printTree(root);
    printf("\n");
    //printf("The Postfix (Reverse Polish) Expression:\n");
    printTreePostfix(root);
    printf("\n");
    //printf("Answer ");
    printf("%.2f\n", computeTree(root));
    deleteTree(&root);
    return 0;
}

char *createExpTree(BTNode **root, char *prefix)
{
    if (prefix == 0)
        return NULL;

    // checks for brackets in case
    while (!strcmp(prefix, "(") || !strcmp(prefix, ")"))
    {
        prefix = strtok(NULL, " ");
    }

    while (1)
    {
        // filling in empty node
        if (*root == NULL)
        {
            BTNode *nullNode = malloc(sizeof(BTNode));
            if (isOperator(prefix))
                nullNode->item = prefix[0];
            // stores integers as negative numbers as operators are never negative
            // prevents conflict if integer is 43 as char '+' is stored as 43 as well
            // just remember to convert back to positive when retrieving it from the node
            else
                nullNode->item = -1 * atoi(prefix);
            nullNode->left = NULL;
            nullNode->right = NULL;
            *root = nullNode;
        }

        else
        {
            // operands are infertile, no child nodes
            if (!isOperator(prefix))
                return prefix;

            // creates children for operator
            // creates left child using next operand/operator
            prefix = createExpTree(&(*root)->left, strtok(NULL, " "));
            // creates right child using next operand/operator
            prefix = createExpTree(&(*root)->right, strtok(NULL, " "));

            // returns updated "string" without previous operand/operator
            return prefix;
        }
    }
}

void printTree(BTNode *node)
{
    if (node == NULL)
        return;

    else
    {
        printTree(node->left);
        if (isOperatorInt(node->item))
            printf("%c ", node->item);
        else
            printf("%d ", -1 * node->item);
        printTree(node->right);
    }
}

void printTreePostfix(BTNode *node)
{
    if (node == NULL)
        return;

    else
    {
        printTreePostfix(node->left);
        printTreePostfix(node->right);
        if (isOperatorInt(node->item))
            printf("%c ", node->item);
        else
            printf("%d ", -1 * node->item);
    }
}

double computeTree(BTNode *node)
{
    if (node == NULL)
        return 0;

    // node is a number
    if (!isOperatorInt(node->item))
        return (double)-1 * node->item;

    // node is operator
    else
    {
        double l = computeTree(node->left),
               r = computeTree(node->right);
        return computeOperation(node->item, l, r);
    }
}

int isOperator(char *c)
{
    if (c == NULL)
        return 0;

    int i, res = 0;
    char OPERATORS[4] = "+-*/";
    for (i = 0; i < 4; i++)
    {
        if (c[0] == OPERATORS[i])
            res = 1;
    }
    return res;
}

int isOperatorInt(int c)
{
    int i, res = 0;
    char OPERATORS[4] = "+-*/";
    for (i = 0; i < 4; i++)
    {
        if (c == OPERATORS[i])
            res = 1;
    }
    return res;
}

double computeOperation(char operator, int op1, int op2)
{
    switch (operator)
    {
    case '+':
        return op1 + op2;
    case '-':
        return op1 - op2;
    case '*':
        return op1 * op2;
    case '/':
        return op1 / op2;
    default:
        return 0;
    }
}

void push(Stack *sPtr, BTNode *item)
{
    StackNode *newNode;
    newNode = malloc(sizeof(StackNode));
    newNode->item = item;
    newNode->next = sPtr->head;
    sPtr->head = newNode;
    sPtr->size++;
}

int pop(Stack *sPtr)
{
    if (sPtr == NULL || sPtr->head == NULL)
    {
        return 0;
    }
    else
    {
        StackNode *temp = sPtr->head;
        sPtr->head = sPtr->head->next;
        free(temp);
        sPtr->size--;
        return 1;
    }
}

BTNode *peek(Stack s)
{
    return s.head->item;
}

int isEmptyStack(Stack s)
{
    if (s.size == 0)
        return 1;
    else
        return 0;
}

void deleteTree(BTNode **root)
{
    BTNode *temp;
    if (*root != NULL)
    {
        temp = (*root)->right;
        deleteTree(&((*root)->left));
        free(*root);
        *root = NULL;
        deleteTree(&temp);
    }
}