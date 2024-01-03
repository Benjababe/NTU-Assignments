#ifndef H_HELPER
#define H_HELPER

#include <chrono>

#include "bpTree.h"
#include "block.h"
#include "disk.h"
#include "structs.h"

uint64_t get_current_time();
uint64_t get_time_taken(uint64_t);
ReadRecordResult read_all_records(Disk &, std::vector<RecordPtr>, std::map<size_t, Block> &);

#endif
