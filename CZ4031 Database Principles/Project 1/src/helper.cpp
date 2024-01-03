#include "helper.h"

uint64_t get_current_time()
{
    using namespace std::chrono;
    return duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
}

uint64_t get_time_taken(uint64_t start_time)
{
    uint64_t end_time = get_current_time();
    return end_time - start_time;
}

/**
 * @brief Reads all records in a vector of RecordPtrs
 *
 * @param disk
 * @param result_ptrs Vector of record pointers to retrieve record data
 * @param data_block_cache Acts as memory, don't fetch from disk if block is in cache
 * @return ReadRecordResult
 */
ReadRecordResult read_all_records(Disk &disk, std::vector<RecordPtr> result_ptrs, std::map<size_t, Block> &data_block_cache)
{
    ReadRecordResult res;
    res.record_count = (float)result_ptrs.size();

    for (RecordPtr ptr : result_ptrs)
    {
        Block result_blk;
        int blk_id = ptr.block_id;

        if (data_block_cache.count(blk_id))
        {
            result_blk = data_block_cache[blk_id];
        }
        else
        {
            result_blk = disk.read_block(blk_id);
            data_block_cache[blk_id] = result_blk;
        }

        Record result_rec = result_blk.read_record(ptr.block_offset);

        res.rating_sum += result_rec.average_rating;
    }

    return res;
}