#include <iostream>

// C   - total capacity
// n   - number of items
// w[] - array of weights
// p[] - array of profits
void P(int C, int n, int w[], int p[])
{
    // DP memory array
    int matrix[n][C + 1];

    // initialise all cells with profit of 0
    for (int i = 0; i < n; i++)
        for (int j = 0; j <= C; j++)
            matrix[i][j] = 0;

    // preprocess first item for all capacities
    for (int tmpC = 0; tmpC <= C; tmpC++)
        matrix[0][tmpC] = (tmpC / w[0]) * p[0];

    // for each item, check for every possible capacity
    // skip first item as that has already been processed
    for (int i = 1; i < n; i++)
    {
        for (int tmpC = 1; tmpC <= C; tmpC++)
        {
            // if item can be taken, compare take and skip value
            // and update table accordingly
            if (w[i] <= tmpC)
            {
                // skip will be the profit of previous item at the current weight
                int skip = matrix[i - 1][tmpC];

                // take will be current item's profit + profit at weight - w[i] of current item
                int take = p[i] + matrix[i][tmpC - w[i]];

                matrix[i][tmpC] = (skip >= take) ? skip : take;
            }

            // if item cannot be taken, just skip
            else
                matrix[i][tmpC] = matrix[i - 1][tmpC];
        }
    }

    int i = n - 1,
        tmpC = C,
        profit = matrix[i][C];

    std::cout << "Max profit: " << profit << std::endl;
    std::cout << "Selected items are: ";

    // loop back until item 1, item 0 will be handled separately
    while (i > 0 && matrix[i][tmpC] >= 0)
    {
        // if current item was taken, find go to previous weight but stay on the same item
        if (matrix[i][tmpC] != matrix[i - 1][tmpC])
        {
            std::cout << i;
            tmpC -= w[i];
            profit -= p[i];

            if (profit > 0)
                std::cout << ", ";
        }

        // if item was skipped, go to previous item
        else
            i -= 1;
    }

    // handling item 0, just reduce until profit = 0
    while (profit > 0)
    {
        std::cout << 0;
        profit -= p[0];

        if (profit > 0)
            std::cout << ", ";
    }
}

int main()
{
    int wa[3] = {4, 6, 8},
        pa[3] = {7, 6, 9},

        wb[3] = {5, 6, 8},
        pb[3] = {7, 6, 9};

    std::cout << "(a):\n";
    P(14, 3, wa, pa);

    std::cout << "\n\n";

    std::cout << "(b):\n";
    P(14, 3, wb, pb);
}