#include <vector>
#include <stdlib.h>

#ifndef ADJ
#define ADJ
class AdjacentList
{
public:
    // takes 2d array as constructor argument to convert into a adjacency list
    AdjacentList(int **matrix, int V)
    {
        // loop the source
        for (int i = 0; i < V; i++)
        {
            std::vector<int *> subList;
            list.push_back(subList);
            // loop adjacent nodes
            for (int j = 0; j < V; j++)
            {
                if (matrix[i][j] != 0)
                {
                    int *tmp = (int *)malloc(sizeof(int) * 2);
                    tmp[0] = j;
                    tmp[1] = matrix[i][j];
                    list[i].push_back(tmp);
                }
            }
        }
    }
    // essentially a triple pointer
    std::vector<std::vector<int *>> list;
};
#endif