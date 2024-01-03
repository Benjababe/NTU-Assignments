#include "block.h"

#define BLOCK_SIZE 200

Block::Block()
{
    this->data = std::vector<char>(BLOCK_SIZE, '\0');
    this->record_count = 0;
    this->node = nullptr;
}

/**
 * @brief Inserts record into the block
 *
 * @param block_offset Address offset to insert record
 * @param record Record to insert
 */
void Block::write_record(int block_offset, Record *record)
{
    std::memcpy(&this->data[block_offset], record, sizeof(Record));
    this->inc_record_count();
}

/**
 * @brief Write node pointer to block
 *
 * @param Node pointer
 */
void Block::writeNode(Node *node)
{
    this->node = node;
}

/**
 * @brief Reads record based off address offset
 *
 * @param block_offset Address offset to read from
 * @return Record
 */
Record Block::read_record(int block_offset)
{
    Record record;
    std::memcpy(&record, &this->data[block_offset], sizeof(Record));
    return record;
}

/**
 * @brief Get node pointer
 *
 * @return Node pointer
 */
Node *Block::getNode()
{
    return this->node;
}

void Block::inc_record_count()
{
    ++this->record_count;
}

size_t Block::get_record_count()
{
    return this->record_count;
}