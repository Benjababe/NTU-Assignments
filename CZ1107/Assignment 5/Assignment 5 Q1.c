#include <stdio.h>
#include <stdlib.h>

#define SIZE 80 //The size of the array

enum ExpType
{
    OPT,
    OPERAND
};

typedef struct _listnode
{
    int item;
    enum ExpType type;
    struct _listnode *next;
} ListNode;

typedef struct _linkedlist
{
    int size;
    ListNode *head;
} LinkedList;

void insertNode(LinkedList *llPtr, int item, enum ExpType type);
int deleteNode(LinkedList *llPtr);
void removeAllNodes(LinkedList *llPtr);
int isEmptyLinkedList(LinkedList ll);

void expressionLL(char *infix, LinkedList *inExpLL);

void printExpLL(LinkedList inExpQ, int seed);

int main()
{
    char infix[SIZE];

    //printf("Enter an infix expression:\n");
    gets(infix);

    LinkedList inExpLL;
    inExpLL.head = NULL;
    inExpLL.size = 0;

    expressionLL(infix, &inExpLL);

    int seed;
    //printf("Enter a seed: \n");
    scanf("%d", &seed);
    printExpLL(inExpLL, seed);

    removeAllNodes(&inExpLL);
    return 0;
}

void expressionLL(char *infix, LinkedList *inExpLL)
{
    char OPERATORS[6] = "+-*/()";
    int i, j, *lastNum = malloc(sizeof(int));
    *lastNum = -1;

    while (infix[i] != '\0')
    {
        char cur = infix[i], type = OPERAND;

        // checks if current char is operator
        for (j = 0; j < 6; j++)
        {
            if (cur == OPERATORS[j])
                type = OPT;
        }

        if (type == OPT)
        {
            if (*lastNum != -1)
            {
                insertNode(inExpLL, *lastNum, OPERAND);
                *lastNum = -1;
            }
            insertNode(inExpLL, cur, type);
        }
        else
        {
            // taking advantage of ascii code in sequence
            int curInDec = cur - '0';
            if (*lastNum == -1)
                *lastNum = curInDec;
            else
                *lastNum = (*lastNum * 10) + curInDec;
        }
        i++;
    }
    if (*lastNum != -1)
        insertNode(inExpLL, *lastNum, OPERAND);
}

void printExpLL(LinkedList inExpLL, int seed)
{
    ListNode *temp = NULL;
    temp = inExpLL.head;
    while (temp != NULL)
    {
        if (temp->type == OPERAND)
            printf(" %d ", temp->item + seed);
        else
            printf(" %c ", (char)(temp->item));
        temp = temp->next;
    }
    printf("\n");
}

void insertNode(LinkedList *LLPtr, int item, enum ExpType type)
{
    ListNode *newNode,
        *cur = LLPtr->head;
    newNode = malloc(sizeof(ListNode));
    if (newNode == NULL)
        exit(0);

    newNode->item = item;
    newNode->type = type;
    newNode->next = NULL;

    if (cur == NULL)
    {
        LLPtr->head = newNode;
        LLPtr->size++;
        return;
    }

    while (cur->next != NULL)
    {
        cur = cur->next;
    }

    cur->next = newNode;
    LLPtr->size++;
}

int deleteNode(LinkedList *LLPtr)
{
    if (LLPtr == NULL || LLPtr->size == 0)
    { //Queue is empty or NULL pointer
        return 0;
    }
    else
    {
        ListNode *temp = LLPtr->head;
        LLPtr->head = LLPtr->head->next;

        free(temp);
        LLPtr->size--;
        return 1;
    }
}

int isEmptyLinkedList(LinkedList ll)
{
    if (ll.size == 0)
        return 1;
    else
        return 0;
}

void removeAllNodes(LinkedList *LLPtr)
{
    while (deleteNode(LLPtr))
        ;
}