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

void insertAdjVertex(ListNode **AdjList, int vertex);
void removeAdjVertex(ListNode **AdjList, int vertex);
int matching(Graph g);

void enqueue(Queue *qPtr, int item);
int dequeue(Queue *qPtr);
int getFront(Queue q);
int isEmptyQueue(Queue q);
void removeAllItemsFromQueue(Queue *qPtr);
void printQ(QueueNode *cur);
//////STACK///////////////////////////////////////////
void push(Stack *sPtr, int vertex);
int pop(Stack *sPtr);
int peek(Stack s);
int isEmptyStack(Stack s);
void removeAllItemsFromStack(Stack *sPtr);
//////////////////////////////////

int main()
{
    int Prj, Std, Mtr; //Project, Student and Mentor;
    int maxMatch;
    scanf("%d %d %d", &Std, &Prj, &Mtr);

    int np, nm; //number of projects and number of mentors

    //build graph
    Graph g;
    g.V = Prj + Std + Mtr;
    g.list = (ListNode **)malloc(sizeof(ListNode *) * (g.V + 2));
    *(g.list) = NULL;
    //Write your code

    int i;

    for (i = 0; i <= g.V + 1; i++)
    {
        g.list[i] = NULL;
    }

    // links source node to projects
    for (i = 1; i <= Prj; i++)
    {
        insertAdjVertex(&g.list[0], i);
    }

    // links projects to sink node
    for (i = (Prj + Std + 1); i <= g.V; i++)
    {
        insertAdjVertex(&g.list[i], (g.V + 1));
    }

    // for each student
    for (i = 1; i <= Std; i++)
    {
        int prjPref, mtrPref, j;

        // get project & mentor preference count
        scanf("%d %d", &np, &nm);

        // links projects preferred to student
        for (j = 0; j < np; j++)
        {
            int prjID;
            scanf("%d", &prjID);
            insertAdjVertex(&g.list[prjID], (i + Prj));
        }

        // links students to preferred mentors
        for (j = 0; j < nm; j++)
        {
            int mtrID;
            scanf("%d", &mtrID);
            insertAdjVertex(&g.list[i + Prj], (Prj + Std + mtrID));
        }
    }

    //apply Ford Fulkerson algorithm
    // use DFS or BFS to find a path
    maxMatch = matching(g);
    printf("%d\n", maxMatch);
    return 0;
}

int matching(Graph g)
{
    int flow[g.V + 2][g.V + 2];

    int count = 0, i, j;

    // create residual graph r, a clone of g
    Graph r;
    r.E = g.E;
    r.V = g.V;
    r.list = (ListNode **)malloc(sizeof(ListNode *) * (r.V + 2));

    for (i = 0; i < (r.V + 2); i++)
    {
        r.list[i] = NULL;
        ListNode *l = g.list[i];
        while (l != NULL)
        {
            insertAdjVertex(&r.list[i], l->vertex);
            l = l->next;
        }
    }

    // init flow matrix with -1
    for (i = 0; i < (g.V + 2); i++)
    {
        for (j = 0; j < (g.V + 2); j++)
        {
            flow[i][j] = -1;
        }
    }

    // fill edges with flow 0
    for (i = 0; i < (g.V + 2); i++)
    {
        ListNode *l = g.list[i];

        while (l != NULL)
        {
            flow[i][l->vertex] = 0;
            flow[l->vertex][i] = 0;
            l = l->next;
        }
    }

    // BFS
    Queue *q = malloc(sizeof(Queue *));
    q->head = NULL;
    q->tail = NULL;
    q->size = 0;

    int predecessor[g.V + 2],
        finished[g.V + 2],
        pathCount = 0;

    for (i = 0; i < (g.V + 2); i++)
    {
        predecessor[i] = -1;
        finished[i] = 0;
    }

    // enqueue source node
    enqueue(q, 0);

    ListNode **paths = (ListNode **)malloc(sizeof(ListNode *) * (g.V + 2));

    while (!isEmptyQueue(*q))
    {
        int w = getFront(*q);
        dequeue(q);

        // if path is found
        if (w == (g.V + 1))
        {
            paths[pathCount] = NULL;
            insertAdjVertex(&(paths[pathCount]), w);

            while (predecessor[w] != -1)
            {
                // sets vertex to be untouchable
                if (w != (g.V + 1) && w != 0)
                {
                    finished[w] = 1;
                }

                // gets previous vertex
                w = predecessor[w];
            }
            ListNode *debug = paths[pathCount];
            pathCount++;
            removeAllItemsFromQueue(q);
        }

        // traverse node if haven't, always traverse if source node
        if (finished[w] == 0 || w == 0)
        {
            ListNode *l = r.list[w];
            while (l != NULL)
            {
                enqueue(q, l->vertex);
                predecessor[l->vertex] = w;
                l = l->next;
            }
        }
    }

    return pathCount;
}

void removeAdjVertex(ListNode **AdjList, int vertex)
{
    ListNode *temp, *preTemp;
    if (*AdjList != NULL)
    {
        // first node
        if ((*AdjList)->vertex == vertex)
        {
            temp = *AdjList;
            *AdjList = (*AdjList)->next;
            free(temp);
            return;
        }
        preTemp = *AdjList;
        temp = (*AdjList)->next;
        while (temp != NULL && temp->vertex != vertex)
        {
            preTemp = temp;
            temp = temp->next;
        }
        preTemp->next = temp->next;
        free(temp);
    }
}
void insertAdjVertex(ListNode **AdjList, int vertex)
{
    ListNode *temp;
    if (*AdjList == NULL)
    {
        *AdjList = (ListNode *)malloc(sizeof(ListNode));
        (*AdjList)->vertex = vertex;
        (*AdjList)->next = NULL;
    }
    else
    {
        temp = (ListNode *)malloc(sizeof(ListNode));
        temp->vertex = vertex;
        temp->next = *AdjList;
        *AdjList = temp;
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

void printQ(QueueNode *cur)
{
    if (cur == NULL)
        printf("Empty");

    while (cur != NULL)
    {
        printf("%d ", cur->vertex);
        cur = cur->next;
    }
    printf("\n");
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