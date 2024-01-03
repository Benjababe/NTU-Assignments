#ifndef H_STRUCTS
#define H_STRUCTS

#include <ostream>

// size of record will be 20 bytes, allowing 10 records per block perfectly
struct Record
{
    char tconst[12];      // 12 bytes, fixed string length
    float average_rating; // 4 bytes
    int num_votes;        // 4 bytes
};

// keeps track of which block the record is stored in
// and where the record starts in the block
struct RecordPtr
{
    int block_id = 0;
    int block_offset = 0;
};

struct ReadRecordResult
{
    float rating_sum = 0;
    float record_count = 0;
};

#endif