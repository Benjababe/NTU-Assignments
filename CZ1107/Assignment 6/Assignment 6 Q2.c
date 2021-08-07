#include <stdio.h>
#include <stdlib.h>

#define TABLESIZE 37
#define PRIME 13

enum Marker
{
    EMPTY,
    USED,
    DELETED
};

typedef struct _slot
{
    int key;
    enum Marker indicator;
} HashSlot;

int HashInsert(int key, HashSlot hashTable[]);
int HashDelete(int key, HashSlot hashTable[]);

int doubleHash(int key, int i);
int hash1(int key);
int hash2(int key);

int main()
{
    int opt;
    int i;
    int key;
    int comparison;
    HashSlot hashTable[TABLESIZE];

    for (i = 0; i < TABLESIZE; i++)
    {
        hashTable[i].indicator = EMPTY;
        hashTable[i].key = 0;
    }

    printf("============= Hash Table ============\n");
    printf("|1. Insert a key to the hash table  |\n");
    printf("|2. Delete a key from the hash table|\n");
    printf("|3. Print the hash table            |\n");
    printf("|4. Quit                            |\n");
    printf("=====================================\n");
    printf("Enter selection: ");
    scanf("%d", &opt);
    while (opt > 0 && opt < 4)
    {
        switch (opt)
        {
        case 1:
            printf("Enter a key to be inserted:\n");
            scanf("%d", &key);
            comparison = HashInsert(key, hashTable);
            if (comparison < 0)
                printf("Duplicate key\n");
            else if (comparison < TABLESIZE)
                printf("Insert: %d Key Comparisons: %d\n", key, comparison);
            else
                printf("Key Comparisons: %d. Table is full.\n", comparison);
            break;
        case 2:
            printf("Enter a key to be deleted:\n");
            scanf("%d", &key);
            comparison = HashDelete(key, hashTable);
            if (comparison < 0)
                printf("%d does not exist.\n", key);
            else if (comparison <= TABLESIZE)
                printf("Delete: %d Key Comparisons: %d\n", key, comparison);
            else
                printf("Error\n");
            break;
        case 3:
            for (i = 0; i < TABLESIZE; i++)
                printf("%d: %d %c\n", i, hashTable[i].key, hashTable[i].indicator == DELETED ? '*' : ' ');
            break;
        }
        printf("Enter selection: ");
        scanf("%d", &opt);
    }
    return 0;
}

int doubleHash(int key, int i)
{
    return hash1(key + i * hash2(key));
}

int hash1(int key)
{
    return (key % TABLESIZE);
}

int hash2(int key)
{
    return (key % PRIME) + 1;
}

int HashInsert(int key, HashSlot hashTable[])
{
    int i, hash, firstAvailable = -1, keyCount = 0;

    for (i = 0; i < TABLESIZE; i++)
    {
        // generate hash w/ double hashing
        hash = (hash1(key) + i * hash2(key)) % TABLESIZE;

        // duplicate key
        if (hashTable[hash].key == key && hashTable[hash].indicator == USED)
            return -1;

        // checks if slot is being used
        if (hashTable[hash].indicator != USED)
        {
            if (firstAvailable == -1)
            {
                firstAvailable = i;
                int h = (hash1(key) + i * hash2(key)) % TABLESIZE;
            }
        }

        else if (firstAvailable == -1 || hashTable[hash].indicator == DELETED)
            keyCount++;
    }

    // if there is an empty slot and item isn't already in table
    if (firstAvailable != -1)
    {
        hash = (hash1(key) + firstAvailable * hash2(key)) % TABLESIZE;
        hashTable[hash].key = key;
        hashTable[hash].indicator = USED;
        return keyCount;
    }

    return i;
}

int HashDelete(int key, HashSlot hashTable[])
{
    int i, hash;

    for (i = 0; i < TABLESIZE; i++)
    {
        hash = (hash1(key) + i * hash2(key)) % TABLESIZE;

        if (hashTable[hash].key == key && hashTable[hash].indicator == USED)
        {
            hashTable[hash].indicator = DELETED;
            return i + 1;
        }
    }

    return -1;
}
