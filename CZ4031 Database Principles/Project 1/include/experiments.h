#include <iostream>
#include <vector>

#include "bpTree.h"
#include "block.h"
#include "disk.h"
#include "helper.h"
#include "structs.h"

void experiment_1(std::vector<RecordPtr> &);
void experiment_2(BPTree &bptree);
void experiment_3(Disk &, BPTree &);
void experiment_4(Disk &, BPTree &);
void experiment_5(Disk &, BPTree &bpTree, int numVotes);