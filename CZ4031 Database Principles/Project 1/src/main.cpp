#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

#include "block.h"
#include "bpTree.h"
#include "disk.h"
#include "experiments.h"
#include "structs.h"

void read_data_file(Disk &, std::vector<RecordPtr> &, BPTree &);

int main()
{
    Disk disk;
    std::vector<RecordPtr> record_ptrs; // to be used for indexing
    BPTree bpTree(record_ptrs, disk);
    read_data_file(disk, record_ptrs, bpTree);

    std::cout << std::endl;
    experiment_1(record_ptrs);
    experiment_2(bpTree);
    experiment_3(disk, bpTree);
    experiment_4(disk, bpTree);
    experiment_5(disk, bpTree, 1000);

    return 0;
}

/**
 * @brief Reads data file and stores the records in the disk
 *
 * @param disk Object used to simulate storage
 * @param record_ptrs List of record pointers, used in B+ tree
 */
void read_data_file(Disk &disk, std::vector<RecordPtr> &record_ptrs, BPTree &bp_tree)
{
    // read data.tsv or sample.tsv
    // sample contains only the first 50k lines so it doesn't
    // take forever to read & insert when testing features
    std::ifstream data_file("./data/data.tsv");
    std::string line;

    // first getline() is to skip the header
    std::getline(data_file, line);

    // loop until EOF
    while (std::getline(data_file, line))
    {
        std::stringstream ss(line);
        Record record;

        // extracts line into record variables
        ss >> record.tconst >> record.average_rating >> record.num_votes;

        // adds record into disk and retrieves its starting address
        RecordPtr record_ptr = disk.add_record(&record);
        record_ptrs.push_back(record_ptr);
    }

    for (RecordPtr record_ptr : record_ptrs)
    {
        Record record = disk.getBlockPtr(record_ptr.block_id)->read_record(record_ptr.block_offset);
        bp_tree.insert(record.num_votes, record_ptr);
    }
}