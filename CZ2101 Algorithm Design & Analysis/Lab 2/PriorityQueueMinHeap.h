#include <iostream>
#include <vector>

using namespace std;

#ifndef P_Q_MIN_HEAP
#define P_Q_MIN_HEAP
class PriorityQueueMinHeap
{
public:
    // empty constructor
    PriorityQueueMinHeap(){};

    // get parent of i node
    int parent(int i) { return (i - 1) / 2; }

    // get left child of i node
    int left(int i) { return (2 * i + 1); }

    // get right child of i node
    int right(int i) { return (2 * i + 2); }

    // checks if i node is a leaf
    bool isLeaf(int i) { return 2 * i >= (_heap.size() - 1) && i < _heap.size(); }

    // checks if i node has left child
    bool hasLeft(int i) { return left(i) < _heap.size(); }

    // checks if i node has right child
    bool hasRight(int i) { return right(i) < _heap.size(); }

	// swap nodes at i and j
    void swap(int i, int j)
    {
        int tmp0 = _heap[i][0],
            tmp1 = _heap[i][1];

        _heap[i][0] = _heap[j][0];
        _heap[i][1] = _heap[j][1];

        _heap[j][0] = tmp0;
        _heap[j][1] = tmp1;
    }

    // sorts itself upwards from i
    void heapifyUp(int i)
    {
        // checks up parent distance is greater than current index
        while (i != 0 && _heap[parent(i)][1] > _heap[i][1])
        {
            // if so, swap and change current index to its parent since its shifted
            swap(i, parent(i));
            i = parent(i);
        }
    }

    // sorts itself downwards from i
    void heapifyDown(int i)
    {
        // keep swapping if node has children
        while (hasLeft(i))
        {
            int smallestChildIndex = -1;
            // if has children, it WILL have a left child
            if (hasLeft(i))
            {
                int leftChild = left(i);
                // it may not have a right child
                if (hasRight(i))
                {
                    int rightChild = right(i);
                    // get the smaller of the left and right children
                    smallestChildIndex = (_heap[leftChild][1] <= _heap[rightChild][1]) ? leftChild : rightChild;
                }
                // no right child
                else
                    smallestChildIndex = leftChild;
            }
            // no children at all
            else
                break;
            if (_heap[i][1] > _heap[smallestChildIndex][1])
            {
                swap(i, smallestChildIndex);
                i = smallestChildIndex;
            }
            // when the smallest child less or equals to i
            else
                break;
        }
    }

    // adds vertex and its distance from source into the priority queue
    void add(int vertex, int distance)
    {
        // inserts vertex, distance pair into heap
        int *tmp = new int[2]{vertex, distance};
        _heap.push_back(tmp);

        // sorts itself upwards
        heapifyUp(_heap.size() - 1);
    }

    // changes the distance of vertex from the source
    void edit(int vertex, int newDistance)
    {
        // loop through the queue to find the vertex and update the distance
        for (int i = 0; i < _heap.size(); i++)
        {
            if (_heap[i][0] == vertex)
            {
                int oldDistance = _heap[i][1];
                _heap[i][1] = newDistance;

                // if new distance if somehow larger than old distance,
                // no choice but to sort itself downwards
                if (newDistance > oldDistance)
                    heapifyDown(i);
                else
                    heapifyUp(i);
                break;
            }
        }
    }

    // returns [vertex, distance] of the shortest distance pair
    int *pop()
    {
        if (_heap.size() == 0)
            return NULL;

        int *smallest = new int[2]{_heap[0][0], _heap[0][1]};
        _heap.erase(_heap.begin());
        // edge case if size = 0 after erasing
        if (_heap.size() > 1)
        {
            swap(0, _heap.size() - 1);
            heapifyDown(0);
        }
        return smallest;
    }

	// returns whether heap is empty
    bool isEmpty()
    {
        return _heap.size() == 0;
    }

    // super useful for debugging heapify, prints heap
    void printHeap()
    {
        for (int i = 0; i < _heap.size(); i++)
        {
            int *tmp = _heap[i];
            cout << "(" << tmp[0] << "," << tmp[1] << ") ";
        }
        cout << endl;
    }

protected:
	// heap stores as vector instead of a tree structure
    vector<int *> _heap;
};
#endif