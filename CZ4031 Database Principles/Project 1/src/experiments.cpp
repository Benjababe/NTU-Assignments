#include "experiments.h"

std::ostream &operator<<(std::ostream &os, const Record &record)
{
    return os << "tconst: " << record.tconst << "\trating: " << record.average_rating << "\tnum votes: " << record.num_votes;
}

void experiment_1(std::vector<RecordPtr> &record_ptrs)
{
    RecordPtr last = record_ptrs[record_ptrs.size() - 1];

    std::cout << "\nExperiment 1:" << std::endl;
    std::cout << "Number of records: " << record_ptrs.size() << std::endl;
    std::cout << "Size of a record: " << sizeof(Record) << " bytes" << std::endl;
    std::cout << "Number of records in a block: " << 200 / sizeof(Record) << std::endl;
    std::cout << "Number of blocks used: " << last.block_id + 1 << std::endl;
}

void experiment_2(BPTree &bpTree)
{
    std::cout << "\nExperiment 2:" << std::endl;
    std::cout << "Parameter n of b+ tree : " << bpTree.maxKeys << std::endl;
    std::cout << "Number of nodes of b+ tree : " << bpTree.numNodes << std::endl;
    std::cout << "Number of levels of b+ tree : " << bpTree.height << std::endl;
    Node *rootNode = bpTree.disk->getBlockPtr(bpTree.getRoot().block_id)->getNode();
    std::cout << "Keys of root node : ";
    for (int i = 0; i < rootNode->numKeys; i++)
    {
        std::cout << rootNode->nodeKeyArr[i];
        if (i + 1 != rootNode->numKeys)
            std::cout << ", ";
    }
    std::cout << std::endl;
}

void experiment_3(Disk &disk, BPTree &bpTree)
{
    std::map<size_t, Block> data_block_cache; // keep track number of blocks read to "memory"
    size_t node_access_count = 0;             // no. of node blocks read
    float rating_sum = 0;
    float record_count = 0;

    // access root node
    ++node_access_count;

    int search_val = 500;
    std::vector<RecordPtr> result_ptrs;

    time_t start_time_index = get_current_time();
    Node *lf_node = bpTree.findLeafNode(search_val, node_access_count);

    // find the pointer to the records
    for (size_t i = 0; i < lf_node->numKeys; i++)
    {
        if (lf_node->nodeKeyArr[i] >= search_val)
        {
            result_ptrs = lf_node->nodeRecordPtrArr[i];
            break;
        }
    }

    ReadRecordResult res = read_all_records(disk, result_ptrs, data_block_cache);
    rating_sum = res.rating_sum;
    record_count = res.record_count;

    size_t blocks_accessed_linear = 0;
    size_t linear_result_count = 0;
    uint64_t time_taken_index = get_time_taken(start_time_index);

    time_t start_time_linear = get_current_time();

    Block block;
    for (size_t i = 0; i <= disk.get_block_idx(); ++i)
    {
        block = disk.read_block(i);
        if (block.get_record_count() == 0)
            break;
        ++blocks_accessed_linear;

        for (size_t r_i = 0; r_i < block.get_record_count(); ++r_i)
        {
            Record record = block.read_record((int)r_i * sizeof(Record));
            if (record.num_votes == 500)
                ++linear_result_count;
        }
    }

    uint64_t time_taken_linear = get_time_taken(start_time_linear);

    std::cout << "\nExperiment 3:" << std::endl;
    std::cout << "Number of records with numVotes=500: " << record_count << std::endl;
    std::cout << "Number of index nodes accessed: " << node_access_count << std::endl;
    std::cout << "Number of data blocks accessed: " << data_block_cache.size() << std::endl;
    std::cout << "Average rating: " << rating_sum / record_count << std::endl;
    std::cout << "Time taken searching using B+ tree: " << time_taken_index << "μs" << std::endl;
    std::cout << "Number of data blocks accessed for linear scan: " << blocks_accessed_linear << std::endl;
    std::cout << "Time taken for linear scan: " << time_taken_linear << "μs" << std::endl;
}

void experiment_4(Disk &disk, BPTree &bpTree)
{
    std::map<size_t, Block> data_block_cache; // keep track number of blocks read to "memory"
    size_t node_access_count = 0;             // no. of node blocks read
    float rating_sum = 0;
    float record_count = 0;

    // access root node
    ++node_access_count;

    int start_search_val = 30000;
    int end_search_val = 40000;
    std::vector<RecordPtr> result_ptrs;

    time_t start_time_index = get_current_time();

    Node *lf_node = bpTree.findLeafNode(start_search_val, node_access_count);

    // find the pointer to the records until leaf node is out of search range
    while (lf_node->nodeKeyArr[0] <= end_search_val)
    {
        // search leaf node for key between 30-40k
        for (size_t i = 0; i < lf_node->numKeys; i++)
        {
            if (start_search_val <= lf_node->nodeKeyArr[i] && lf_node->nodeKeyArr[i] <= end_search_val)
            {
                result_ptrs = lf_node->nodeRecordPtrArr[i];
                ReadRecordResult res = read_all_records(disk, result_ptrs, data_block_cache);
                rating_sum += res.rating_sum;
                record_count += res.record_count;
            }
        }

        // quit if current leaf node is the end
        if (lf_node->nodeKeyArr[lf_node->numKeys - 1] > end_search_val)
            break;

        // go to next leaf node
        RecordPtr ptr = lf_node->nodeRecordPtrArr[lf_node->nodeRecordPtrArr.size() - 1][0];
        Block tmp_block = disk.read_block(ptr.block_id);
        lf_node = tmp_block.getNode();
        ++node_access_count;
    }

    size_t blocks_accessed_linear = 0;
    size_t linear_result_count = 0;
    uint64_t time_taken_index = get_time_taken(start_time_index);

    time_t start_time_linear = get_current_time();

    Block block;
    for (size_t i = 0; i <= disk.get_block_idx(); ++i)
    {
        block = disk.read_block(i);
        if (block.get_record_count() == 0)
            break;
        ++blocks_accessed_linear;

        for (size_t r_i = 0; r_i < block.get_record_count(); ++r_i)
        {
            Record record = block.read_record((int)r_i * sizeof(Record));
            if (start_search_val <= record.num_votes && record.num_votes <= end_search_val)
                ++linear_result_count;
        }
    }

    uint64_t time_taken_linear = get_time_taken(start_time_linear);

    std::cout << "\nExperiment 4:" << std::endl;
    std::cout << "Number of records from 30,000 to 40,000: " << record_count << std::endl;
    std::cout << "Number of index nodes accessed: " << node_access_count << std::endl;
    std::cout << "Number of data blocks accessed: " << data_block_cache.size() << std::endl;
    std::cout << "Average rating: " << rating_sum / record_count << std::endl;
    std::cout << "Time taken searching using B+ tree: " << time_taken_index << "μs" << std::endl;
    std::cout << "Number of data blocks accessed for linear scan: " << blocks_accessed_linear << std::endl;
    std::cout << "Time taken for linear scan: " << time_taken_linear << "μs" << std::endl;
}

void experiment_5(Disk &disk, BPTree &bpTree, int numVotes)
{
    time_t start_time_delete = get_current_time();
    time_t start_time_index = get_current_time();
    bpTree.deleteNode(numVotes);
    uint64_t time_taken_delete = get_time_taken(start_time_delete);

    std::map<size_t, Block> data_block_cache;
    std::vector<RecordPtr> result_ptrs;
    ReadRecordResult res = read_all_records(disk, result_ptrs, data_block_cache);

    size_t blocks_accessed_linear = 0;
    size_t linear_result_count = 0;
    uint64_t time_taken_index = get_time_taken(start_time_index);
    time_t start_time_linear = get_current_time();

    Block block;
    for (size_t i = 0; i <= disk.get_block_idx(); ++i)
    {
        block = disk.read_block(i);
        if (block.get_record_count() == 0)
            break;
        ++blocks_accessed_linear;

        for (size_t r_i = 0; r_i < block.get_record_count(); ++r_i)
        {
            Record record = block.read_record((int)r_i * sizeof(Record));
            if (record.num_votes == 1000)
                ++linear_result_count;
        }
    }

    uint64_t time_taken_linear = get_time_taken(start_time_linear);

    std::cout << "\nExperiment 5:" << std::endl;
    std::cout << "number of nodes of b+ tree : " << bpTree.numNodes << std::endl;
    std::cout << "number of levels of b+ tree : " << bpTree.height << std::endl;
    Node *rootNode = bpTree.disk->getBlockPtr(bpTree.getRoot().block_id)->getNode();
    std::cout << "Keys of root node : ";
    for (int i = 0; i < rootNode->numKeys; i++)
    {
        std::cout << rootNode->nodeKeyArr[i];
        if (i + 1 != rootNode->numKeys)
            std::cout << ", ";
    }
    std::cout << std::endl;
    std::cout << "Time taken to delete a node : " << time_taken_delete << "μs" << std::endl;
    std::cout << "Time taken searching using B+ tree: " << time_taken_index << "μs" << std::endl;
    std::cout << "Number of data blocks accessed for linear scan: " << blocks_accessed_linear << std::endl;
    std::cout << "Time taken for linear scan: " << time_taken_linear << "μs" << std::endl;
}