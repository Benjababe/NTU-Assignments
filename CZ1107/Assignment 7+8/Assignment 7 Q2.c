#include <stdio.h>
#include <stdlib.h>

typedef struct _listnode
{
    int vertex;
    struct _listnode *next;
} ListNode;
typedef ListNode StackNode;

typedef struct _graph
{
    int V;
    int E;
    ListNode **list;
} Graph;

typedef ListNode QueueNode;

typedef struct _queue
{
    int size;
    QueueNode *head;
    QueueNode *tail;
} Queue;

typedef struct _stack
{
    int size;
    StackNode *head;
} Stack;

int CC(Graph g);
int BFS(Graph G, int v, int w);

void printGraphList(Graph);

// You should not change the prototypes of these functions
void enqueue(Queue *qPtr, int item);
int dequeue(Queue *qPtr);
int getFront(Queue q);
int isEmptyQueue(Queue q);
void removeAllItemsFromQueue(Queue *qPtr);
//////STACK///////////////////////////////////////////
void push(Stack *sPtr, int vertex);
int pop(Stack *sPtr);
int peek(Stack s);
int isEmptyStack(Stack s);
void removeAllItemsFromStack(Stack *sPtr);
//////////////////////////////////

int main()
{
    Graph g;
    int i, j;
    ListNode *temp;

    printf("Enter the number of vertices:\n");
    scanf("%d", &g.V);

    g.list = (ListNode **)malloc(g.V * sizeof(ListNode *));

    for (i = 0; i < g.V; i++)
        g.list[i] = NULL;

    printf("Enter two vertices which are adjacent to each other:\n");
    while (scanf("%d %d", &i, &j) == 2)
    {
        i = i - 1;

        if (g.list[i] == NULL)
        {
            g.list[i] = (ListNode *)malloc(sizeof(ListNode));
            g.list[i]->vertex = j;
            g.list[i]->next = NULL;
        }
        else
        {
            temp = (ListNode *)malloc(sizeof(ListNode));
            temp->next = g.list[i];
            temp->vertex = j;
            g.list[i] = temp;
        }
        g.E++;
        printf("Enter two vertices which are adjacent to each other:\n");
    }
    scanf("%*c");

    int res = CC(g);
    if (res == 1)
        printf("The graph is strongly connected.\n");
    else
        printf("The graph is not strongly connected.\n");

    printGraphList(g);
    return 0;
}

int CC(Graph g)
{
    int i, j;
    for (i = 1; i <= g.V; i++)
    {
        for (j = 1; j <= g.V; j++)
        {
            // if vertices are the same, skip
            if (i == j)
                continue;
            // if no path is found between vertices i and j
            // graph isn't strongly connected
            // using BFS algo from Q1
            if (BFS(g, i, j) == -1)
                return 0;
        }
    }
    return 1;
}

int BFS(Graph g, int v, int w)
{
    Queue *q = malloc(sizeof(Queue));
    q->head = NULL;
    q->tail = NULL;
    q->size = 0;

    int predecessor[g.V],
        traversed[g.V],
        distance[g.V],
        i = 0,
        found = 0;

    for (i = 0; i < g.V; i++)
    {
        predecessor[i] = -1;
        traversed[i] = 0;
        distance[i] = __INT_MAX__;
    }

    traversed[v - 1] = 1;
    distance[v - 1] = 0;
    enqueue(q, v);

    while (!isEmptyQueue(*q) && !found)
    {

        // gets front of queue and removes it
        v = getFront(*q);
        dequeue(q);

        // list of all vertices connected to vertex v
        ListNode *E = g.list[v - 1];
        while (E != NULL)
        {

            // -1 because of index
            int node = E->vertex - 1;

            // if vertex hasn't been traversed before
            if (traversed[node] == 0)
            {
                traversed[node] = 1;

                // distance from source is previous vertex + 1
                distance[node] = distance[v - 1] + 1;

                // keeps the vertex before this one
                predecessor[node] = v;

                // adds vertex to queue
                enqueue(q, node + 1);

                // if vertex is the destination, exit
                if (E->vertex == w)
                {
                    found = 1;
                    break;
                }
            }
            // goes to next vertex connected to V
            E = E->next;
        }
    }

    return (found) ? distance[w - 1] : -1;
}

void printGraphList(Graph g)
{
    int i;
    ListNode *temp;

    for (i = 0; i < g.V; i++)
    {
        printf("%d:\t", i + 1);
        temp = g.list[i];
        while (temp != NULL)
        {
            printf("%d -> ", temp->vertex);
            temp = temp->next;
        }
        printf("\n");
    }
}

void enqueue(Queue *qPtr, int vertex)
{
    QueueNode *newNode;
    newNode = malloc(sizeof(QueueNode));
    if (newNode == NULL)
        exit(0);

    newNode->vertex = vertex;
    newNode->next = NULL;

    if (isEmptyQueue(*qPtr))
        qPtr->head = newNode;
    else
        qPtr->tail->next = newNode;

    qPtr->tail = newNode;
    qPtr->size++;
}

int dequeue(Queue *qPtr)
{
    if (qPtr == NULL || qPtr->head == NULL)
    { //Queue is empty or NULL pointer
        return 0;
    }
    else
    {
        QueueNode *temp = qPtr->head;
        qPtr->head = qPtr->head->next;
        if (qPtr->head == NULL) //Queue is emptied
            qPtr->tail = NULL;

        free(temp);
        qPtr->size--;
        return 1;
    }
}

int getFront(Queue q)
{
    return q.head->vertex;
}

int isEmptyQueue(Queue q)
{
    if (q.size == 0)
        return 1;
    else
        return 0;
}

void removeAllItemsFromQueue(Queue *qPtr)
{
    while (dequeue(qPtr))
        ;
}

void push(Stack *sPtr, int vertex)
{
    StackNode *newNode;
    newNode = malloc(sizeof(StackNode));
    newNode->vertex = vertex;
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

int isEmptyStack(Stack s)
{
    if (s.size == 0)
        return 1;
    else
        return 0;
}

int peek(Stack s)
{
    return s.head->vertex;
}

void removeAllItemsFromStack(Stack *sPtr)
{
    while (pop(sPtr))
        ;
}
