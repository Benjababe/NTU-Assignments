#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 80 //The size of the array

enum ExpType
{
    OPERAND,
    OPT
};

typedef struct _stackNode
{
    int item;
    struct _stackNode *next;
} StackNode;

typedef struct _stack
{
    int size;
    StackNode *head;
} Stack;

void push(Stack *sPtr, int item);
int pop(Stack *sPtr);
int peek(Stack s);
int isEmptyStack(Stack s);

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
ListNode *deleteNode(LinkedList *llPtr);
void removeAllNodes(LinkedList *llPtr);
int isEmptyLinkedList(LinkedList ll);

void in2PreLL(char *infix, LinkedList *inExpLL);
void popToLL(Stack *s, LinkedList *ll);
int checkPrecedence(char c, char S);
int getPriority(char c);
int isOperator(int c);
char *reverse(char *str);

void printExpLL(LinkedList inExp);

int main()
{
    char infix[SIZE];

    //printf("Enter an infix expression:\n");
    gets(infix);

    LinkedList inExpLL;
    inExpLL.head = NULL;
    inExpLL.size = 0;

    in2PreLL(infix, &inExpLL);

    printExpLL(inExpLL);

    removeAllNodes(&inExpLL);
    return 0;
}

void in2PreLL(char *infix, LinkedList *inExpLL)
{
    // doing the following according to the internet:
    // 1. reverse infix expression, swapping '(' and ')'
    // 2. run through postfix algorithm
    // 3. reverse the postfix expression
    // 4. profit

    LinkedList *tempLL = malloc(sizeof(LinkedList));
    tempLL->head = NULL;
    tempLL->size = 0;

    Stack *s = malloc(sizeof(Stack));
    s->head = NULL;
    s->size = 0;

    char OPERATORS[6] = "+-*/()",
         *lastNumber = "";
    int i = 0, j = 0;
    reverse(infix);

    while (infix[i] != '\0')
    {
        char cur = infix[i],
             type = isOperator(cur);

        // skips space if any happens to be there
        if (cur == ' ')
        {
            i++;
            continue;
        }

        if (type == OPT)
        {
            // if is operand / number
            if (strlen(lastNumber) > 0)
            {
                int num = atoi(lastNumber);
                insertNode(inExpLL, num, OPERAND);
                strcpy(lastNumber, "");
            }

            if (cur == ')')
            {
                while (peek(*s) != '(')
                {
                    popToLL(s, inExpLL);
                }
                pop(s);
            }

            else if (cur == '(')
            {
                push(s, cur);
            }

            // if is regular operator
            // condition checking is longwinded because debugging
            else
            {
                int cond1 = !isEmptyStack(*s), cond2 = 0, cond3 = 0;
                if (cond1)
                {
                    cond2 = peek(*s) != '(';
                    cond3 = checkPrecedence(cur, peek(*s));
                }
                while (cond1 && cond2 && cond3)
                {
                    popToLL(s, inExpLL);

                    cond1 = !isEmptyStack(*s);
                    if (cond1)
                    {
                        cond2 = peek(*s) != '(';
                        cond3 = checkPrecedence(cur, peek(*s));
                    }
                }
                push(s, cur);
            }
        }

        // since infix is reversed, prepends current char to saved number
        else
        {
            // sprintf expects free memory space apparently
            char *test = malloc(sizeof(char) * 20);
            sprintf(test, "%d", (cur - '0'));
            strcat(test, lastNumber);

            lastNumber = malloc(sizeof(char) * 20);
            strcpy(lastNumber, test);
        }
        i++;
    }

    // in case last item is a number
    if (strlen(lastNumber) > 0)
        push(s, atoi(lastNumber));

    while (!isEmptyStack(*s))
    {
        popToLL(s, inExpLL);
    }
}

void popToLL(Stack *s, LinkedList *ll)
{
    int item = pop(s),
        type = isOperator(item);
    insertNode(ll, item, type);
}

// where c is current, S is the popped operator
int checkPrecedence(char c, char S)
{
    char prioC = getPriority(c),
         prioS = getPriority(S);

    // special case for infix->prefix,
    // only pop operators of greater precedence
    // this took 3 hours to figure out holy hell
    return (prioS > prioC);
}

int getPriority(char c)
{
    if (c == '-' || c == '+')
        return 1;
    else if (c == '*' || c == '/')
        return 2;
    else if (c == '^')
        return 3;
    return 0;
}

int isOperator(int c)
{
    int i, res = OPERAND;
    char OPERATORS[6] = "+-*/()";

    for (i = 0; i < 6; i++)
    {
        if (c == OPERATORS[i])
            res = OPT;
    }

    return res;
}

char *reverse(char *str)
{
    int i = strlen(str),
        j = 0;
    char temp[i];

    for (i = i - 1, j; (i + 1) != 0; --i, ++j)
    {
        if (str[i] == '(')
            temp[j] = ')';
        else if (str[i] == ')')
            temp[j] = '(';
        else
            temp[j] = str[i];
    }

    temp[j] = '\0';
    strcpy(str, temp);
    return str;
}

void printExpLL(LinkedList inExpLL)
{
    ListNode *temp = NULL;
    temp = inExpLL.head;
    while (temp != NULL)
    {
        if (temp->type == OPERAND)
            printf(" %d ", temp->item);
        else
            printf(" %c ", (char)(temp->item));
        temp = temp->next;
    }
    printf("\n");
}

void insertNode(LinkedList *LLPtr, int item, enum ExpType type)
{
    ListNode *newNode;
    newNode = malloc(sizeof(ListNode));
    if (newNode == NULL)
        exit(0);

    newNode->item = item;
    newNode->type = type;
    newNode->next = LLPtr->head;
    LLPtr->head = newNode;
    LLPtr->size++;
}

ListNode *deleteNode(LinkedList *LLPtr)
{
    if (LLPtr == NULL || LLPtr->size == 0)
    {
        return 0;
    }
    else
    {
        ListNode *temp = LLPtr->head;
        LLPtr->head = LLPtr->head->next;

        LLPtr->size--;
        return temp;
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

void push(Stack *sPtr, int item)
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
        int val = sPtr->head->item;
        StackNode *temp = sPtr->head;
        sPtr->head = sPtr->head->next;
        free(temp);
        sPtr->size--;
        return val;
    }
}

int peek(Stack s)
{
    int item = s.head->item;
    return item;
}

int isEmptyStack(Stack s)
{
    if (s.size == 0)
        return 1;
    else
        return 0;
}