#include "disk.h"

#define BLOCK_SIZE 200

Disk::Disk()
{
    // queries for disk size
    int memory_mb = 0;
    while (memory_mb < 100 || memory_mb > 500)
    {
        std::cout << "Disk size in MB (100-500): ";
        std::cin >> memory_mb;
    }

    this->block_idx = 0;    // points to block
    this->block_offset = 0; // points to record
    this->record_size = sizeof(Record);
    this->memory_size = memory_mb * 1000000;
    this->block_count = this->memory_size / BLOCK_SIZE;

    // initialise disk full of 0s
    Block empty_block;
    this->blocks = std::vector<Block>(this->block_count, empty_block);
}

size_t Disk::get_block_idx()
{
    return this->block_idx;
}

/**
 * @brief
 * Finds empty address that can fit object of given size.
 * Updates the block_idx and block_offset accordingly.
 *
 * @param size
 */
bool Disk::get_empty_address()
{
    if (this->record_size > BLOCK_SIZE)
    {
        std::cout << "Record size is larger than block size, unable to store it." << std::endl;
        return false;
    }

    // record size + current block allocation is larger than block size
    // move to next block
    else if ((this->block_offset + this->record_size) > BLOCK_SIZE)
    {
        if (++this->block_idx >= this->block_count)
        {
            std::cout << "Reached end of blocks, no more records can be stored" << std::endl;
            return false;
        }

        // reset block pointer when moving to new block
        this->block_offset = 0;
    }

    // does nothing if current block can support the incoming record

    return true;
}

/**
 * @brief Stores record in disk and returns the record's address
 *
 * @param record Pointer of the record data
 * @return RecordPtr Struct containing block index & offset to retrieve the record
 */
RecordPtr Disk::add_record(Record *record)
{
    RecordPtr record_ptr;

    if (this->get_empty_address())
    {
        Block *block = &this->blocks[this->block_idx];
        block->write_record(this->block_offset, record);

        record_ptr.block_id = this->block_idx;
        record_ptr.block_offset = this->block_offset;

        // increment block offset by record size inserted
        this->block_offset += this->record_size;
    }

    return record_ptr;
}

/**
 * @brief Store node in disk
 *
 * @param node pointer
 * @return RecordPtr of block
 */
RecordPtr Disk::addNode(Node *node)
{
    RecordPtr record_ptr;
    this->block_idx++;
    Block *block = &this->blocks[this->block_idx];
    block->writeNode(node);

    record_ptr.block_id = this->block_idx;
    record_ptr.block_offset = 0;

    return record_ptr;
}

/**
 * @brief Returns block object of specified index
 *
 * @param block_id
 * @return Block
 */
Block Disk::read_block(size_t block_id)
{
    return this->blocks[block_id];
}

/**
 * @brief get pointer to block object
 *
 * @param block_id
 * @return Block pointer
 */
Block *Disk::getBlockPtr(int block_id)
{
    return &this->blocks[block_id];
}

/**
 * @brief get pointer to node object
 *
 * @param block pointer
 * @return Node pointer
 */
Node *Disk::getNodePtr(Block *block)
{
    return block->getNode();
}