#ifndef H_BLOCK
#define H_BLOCK

#include <cstring>
#include <vector>

#include "structs.h"
#include "bpTree.h"

class Node;
class Block
{
public:
    Block();
    void write_record(int, Record *);
    Record read_record(int);
    void writeNode(Node *node);
    Node *getNode();
    void inc_record_count();
    size_t get_record_count();

private:
    std::vector<char> data;
    size_t record_count;
    Node *node;
};

#endif