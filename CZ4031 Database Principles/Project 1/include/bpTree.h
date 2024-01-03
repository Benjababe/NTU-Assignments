#ifndef H_BTREE
#define H_BTREE

#include <iostream>
#include <vector>
#include <map>

#include "disk.h"

class Disk;
class Block;

class Node
{
public:
    int numKeys;                                          // Current number of keys in node
    bool isLeaf;                                          // If node is a leaf node
    std::vector<std::vector<RecordPtr> > nodeRecordPtrArr; // Array of RecordPtr
    std::vector<int> nodeKeyArr;                          // Array of key values
    Node(int maxKeys, bool isLeaf);

private:
};

class BPTree
{
public:
    int maxKeys;  // Maximum number of keys
    int numNodes; // Number of nodes in this B+ Tree.
    int height;   // Levels in this B+ Tree.
    Disk *disk;
    BPTree(std::vector<RecordPtr> &, Disk &);
    void insert(int numVotes, RecordPtr recordPointer);
    void updateParentNode(Node *parentNode, Node *newNode, int lastNodeIndex, int minKeys, RecordPtr newPointer, RecordPtr parentPointer, std::vector<RecordPtr> &parentRecordPtr);
    RecordPtr splitParentNode(Node *parentNode, int lastNodeIndex, int minKeys, RecordPtr newPointer);
    void sortLeafNode(Node *curNode, int end);
    int getIndexToInsert(int numVotes, Node *curNode);
    int getSmallestKeyInSubtree(RecordPtr parent);
    RecordPtr getRoot();
    Node *findLeafNode(int, size_t &);
    int getNumLeafNodes();
    std::vector<RecordPtr> addLeftRight(int left, int right, std::vector<RecordPtr> parentRecordPtr, Node *curNode);
    void deleteNode(int numVotes);
    void updateParentNodes(std::vector<RecordPtr> &parentRecordPtr, int numVotestemp, int newVotes);
    void FixInternal(std::vector<RecordPtr> parentRecordPtr, RecordPtr deletedPtr);
    int Traverse(RecordPtr traversePtr);

private:
    RecordPtr root; // pointer to block that contains root node
};

#endif