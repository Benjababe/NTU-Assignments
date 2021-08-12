#include <stdio.h>
#include <stdlib.h>

typedef struct _arraynode
{
	int *itemArray;
	int sizeArray;
	struct _arraynode *next;
} ArrayNode;

typedef struct _arraylist
{
	int size; //the size of a possible sequence
	ArrayNode *head;
} ArrayList;

typedef struct _listnode
{
	int item;
	struct _listnode *next;
} ListNode;

typedef struct _linkedlist
{
	int sum; //the number of possible sequences
	int size;
	ListNode *head;
} LinkedList;

// You should not change the prototypes of these functions
//////LinkedList///////////////////////////////////////////
int insertNode(LinkedList *ll, int index, int coin);
int removeNode(LinkedList *ll, int index);
ListNode *findNode(LinkedList ll, int index);
void removeAllItems(LinkedList *ll);
///////////////////////////////////////////////////

void sumToC(LinkedList *ll, int C, ArrayList *al);
void cloneLL(LinkedList prev, LinkedList *ll);
void findSums(LinkedList *ll, int start, int target, int lastIndex, ArrayList *al);
void insertLLToAL(LinkedList *ll, ArrayList *al);

int main()
{
	int C;
	printf("Enter a number:\n");
	scanf("%d", &C);

	LinkedList ll;
	ll.head = NULL;
	ll.sum = 0;
	ll.size = 0;
	ArrayList al;
	al.head = NULL;
	al.size = 0;

	sumToC(&ll, C, &al);

	//printing all possible sequences
	ArrayNode *temp;
	int i, j;
	temp = al.head;
	for (i = 0; i < al.size; i++)
	{
		for (j = 0; j < temp->sizeArray; j++)
			printf(" %d ", temp->itemArray[j]);
		printf("\n");
		temp = temp->next;
	}

	return 0;
}

void sumToC(LinkedList *ll, int C, ArrayList *al)
{
	int i;
	for (i = 1; i <= C; i++)
	{
		// resets values after every iteration just in case it didn't
		int lastIndex = 0;
		removeAllItems(ll);
		insertNode(ll, lastIndex++, i);
		findSums(ll, i, C, lastIndex, al);
	}
}

void findSums(LinkedList *ll, int start, int target, int lastIndex, ArrayList *al)
{
	// using instanced linked list for current function call
	LinkedList *prevLL = malloc(sizeof(LinkedList));
	// using = doesn't work, have to loop through entire LL adding 1 by 1
	cloneLL(*ll, prevLL);

	// if inserting from prior function call already meets requirement, end it
	if (start == target)
	{
		insertLLToAL(prevLL, al);
		lastIndex = 0;
		return;
	}

	int i;

	// loop through every remaining number
	for (i = start + 1; i <= target; i++)
	{
		int remainder = (target - prevLL->sum);

		// if current number is larger or equals to remainder/2, do not add since there's no possible combination for it
		if ((float)i < ((float)remainder / 2) && prevLL->sum < target)
		{
			insertNode(ll, lastIndex++, i);
			findSums(ll, i, target, lastIndex--, al);
			// sets LL to the way it was before going deeper into the rabbit hole
			cloneLL(*prevLL, ll);
		}

		// if current number is enough to meet the sum, end it
		else if (i == remainder)
		{
			insertNode(ll, lastIndex++, i);
			insertLLToAL(ll, al);
			return;
		}
	}
}

// function to clone the linked list
void cloneLL(LinkedList source, LinkedList *dest)
{
	dest->head = NULL;
	dest->size = 0;
	dest->sum = 0;

	ListNode *cur = source.head;
	int i = 0;
	while (cur != NULL)
	{
		insertNode(dest, i++, cur->item);
		cur = cur->next;
	}
}

// function to insert the linked list into the arraylist
void insertLLToAL(LinkedList *ll, ArrayList *al)
{
	int j = 0;

	// declare new arraynode
	ArrayNode *temp = malloc(sizeof(ArrayNode));
	temp->next = NULL;
	temp->itemArray = malloc(sizeof(int) * ll->size);
	temp->sizeArray = ll->size;

	ListNode *cur = ll->head;

	while (cur != NULL)
	{
		temp->itemArray[j++] = cur->item;
		cur = cur->next;
	}

	ArrayNode *tmp = al->head;
	if (al->head == NULL)
	{
		al->head = temp;
	}

	else
	{
		while (tmp->next != NULL)
		{
			tmp = tmp->next;
		}
		tmp->next = temp;
	}

	al->size++;

	removeAllItems(ll);
	return;
}

///////////////////////////////////////////////////////
int insertNode(LinkedList *ll, int index, int value)
{

	ListNode *pre, *cur;

	if (ll == NULL || index < 0 || index > ll->size)
		return 0;

	if (index == 0)
	{
		cur = ll->head;
		ll->head = (ListNode *)malloc(sizeof(ListNode));
		ll->head->item = value;
		ll->head->next = cur;
		ll->sum += value;
		ll->size++;
		return 1;
	}

	// Find the nodes before and at the target position
	// Create a new node and reconnect the links
	if ((pre = findNode(*ll, index - 1)) != NULL)
	{
		cur = pre->next;
		pre->next = malloc(sizeof(ListNode));
		pre->next->item = value;
		pre->next->next = cur;
		ll->sum += value;
		ll->size++;
		return 1;
	}

	return 0;
}

int removeNode(LinkedList *ll, int index)
{

	ListNode *pre, *cur;

	// Highest index we can remove is size-1
	if (ll == NULL || index < 0 || index > ll->size)
		return 0;

	// If removing first node, need to update head pointer
	if (index == 0)
	{
		cur = ll->head->next;
		ll->sum -= ll->head->item;
		free(ll->head);
		ll->head = cur;
		ll->size--;
		return 1;
	}

	// Find the nodes before and after the target position
	// Free the target node and reconnect the links
	if ((pre = findNode(*ll, index - 1)) != NULL)
	{

		if (pre->next == NULL)
			return 0;

		cur = pre->next;
		ll->sum -= cur->item;
		pre->next = cur->next;
		free(cur);
		ll->size--;
		return 1;
	}

	return 0;
}

ListNode *findNode(LinkedList ll, int index)
{

	ListNode *temp;

	if (index < 0 || index >= ll.size)
		return NULL;

	temp = ll.head;

	if (temp == NULL || index < 0)
		return NULL;

	while (index > 0)
	{
		temp = temp->next;
		if (temp == NULL)
			return NULL;
		index--;
	}

	return temp;
}

void removeAllItems(LinkedList *ll)
{
	ListNode *cur = ll->head;
	ListNode *tmp;

	while (cur != NULL)
	{
		tmp = cur->next;
		free(cur);
		cur = tmp;
	}
	ll->head = NULL;
	ll->size = 0;
	ll->sum = 0;
}
