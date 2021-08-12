#include <stdio.h>
#include <stdlib.h>

#define TABLESIZE 37
#define PRIME 13

enum Marker
{
    EMPTY,
    USED
};

typedef struct _slot
{
    int key;
    enum Marker indicator;
    int next;
} HashSlot;

int HashInsert(int key, HashSlot hashTable[]);
int HashFind(int key, HashSlot hashTable[]);

int hash(int key)
{
    return (key % TABLESIZE);
}

int main()
{
    int opt;
    int i;
    int key;
    int index;
    HashSlot hashTable[TABLESIZE];

    for (i = 0; i < TABLESIZE; i++)
    {
        hashTable[i].next = -1;
        hashTable[i].key = 0;
        hashTable[i].indicator = EMPTY;
    }

    printf("============= Hash Table ============\n");
    printf("|1. Insert a key to the hash table  |\n");
    printf("|2. Search a key in the hash table  |\n");
    printf("|3. Print the hash table            |\n");
    printf("|4. Quit                            |\n");
    printf("=====================================\n");

    printf("Enter selection: ");
    scanf("%d", &opt);
    while (opt >= 1 && opt <= 3)
    {
        switch (opt)
        {
        case 1:
            printf("Enter a key to be inserted:\n");
            scanf("%d", &key);
            index = HashInsert(key, hashTable);
            if (index < 0)
                printf("Duplicate key\n");
            else if (index < TABLESIZE)
                printf("Insert %d at index %d\n", key, index);
            else
                printf("Table is full.\n");
            break;
        case 2:
            printf("Enter a key for searching in the HashTable:\n");
            scanf("%d", &key);
            index = HashFind(key, hashTable);

            if (index != -1)
                printf("%d is found at index %d.\n", key, index);
            else
                printf("%d is not found.\n", key);
            break;

        case 3:
            printf("index:\t key \t next\n");
            for (i = 0; i < TABLESIZE; i++)
                printf("%d\t%d\t%d\n", i, hashTable[i].key, hashTable[i].next);
            break;
        }
        printf("Enter selection: ");
        scanf("%d", &opt);
    }
    return 0;
}

int HashInsert(int key, HashSlot hashTable[])
{
    int i,
        inserted = 0,
        h = hash(key),
        prevHash = -1;

    while (!inserted)
    {
        // slot is open, insert
        if (hashTable[h].indicator != USED)
        {
            hashTable[h].key = key;
            hashTable[h].indicator = USED;
            hashTable[h].next = -1;
            return h;
        }

        // slot is occupied
        else
        {
            // if key already exists
            if (hashTable[h].key == key)
                return -1;
            prevHash = h;
            h = hashTable[h].next;
            // if trail ends here without inserting
            if (h == -1)
                break;
        }
    }

    if (!inserted)
    {
        for (i = prevHash; i < TABLESIZE; i++)
        {
            if (hashTable[i].indicator != USED)
            {
                hashTable[i].key = key;
                hashTable[i].indicator = USED;
                hashTable[i].next = -1;
                // points last referenced index to this one
                hashTable[prevHash].next = i;
                return i;
            }
        }
    }
    return __INT_MAX__;
}

int HashFind(int key, HashSlot hashTable[])
{
    int h = hash(key);

    while (1)
    {
        HashSlot slot = hashTable[h];
        // if slot is used
        if (slot.indicator == USED)
        {
            if (slot.key == key)
                return h;
            // end of the line, key not found
            else if (slot.next == -1)
                return -1;
            else
                h = slot.next;
        }

        // no traces of hash usage at all
        else
            return -1;
    }

    return -1;
}
