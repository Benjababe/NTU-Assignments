#include <vector>

#ifndef P_Q_ARR
#define P_Q_ARR
class PriorityQueueArray
{
public:
    // empty constructor
    PriorityQueueArray(){};

    // adds vertex and its distance from source into the priority queue
    void add(int vertex, int distance)
    {
        int *tmp = new int[2]{vertex, distance};
        queue.push_back(tmp);
    }

    // changes the distance of vertex from the source
    void edit(int vertex, int newDistance)
    {
        // loop through the queue to find the vertex and update the distance
        for (int i = 0; i < queue.size(); i++)
        {
            if (queue[i][0] == vertex)
            {
                queue[i][1] = newDistance;
                break;
            }
        }
    }

    // returns [vertex, distance] of the shortest distance pair
    int *pop()
    {
        // default shortest vertex is 0
        // loop through queue, set smallest index and vertex if needed
        int smallestIndex = 0, *smallestPair = queue[0];
        for (int i = 0; i < queue.size(); i++)
        {
            if (queue[i][1] < queue[smallestIndex][1])
            {
                smallestIndex = i;
                smallestPair = queue[i];
            }
        }
        // removes vertex from queue
        queue.erase(queue.begin() + smallestIndex);
        return smallestPair;
    }
    bool isEmpty()
    {
        return queue.size() == 0;
    }

protected:
    // supposed to use an array but vectors are close enough and easier to work with
    std::vector<int *> queue;
};
#endif