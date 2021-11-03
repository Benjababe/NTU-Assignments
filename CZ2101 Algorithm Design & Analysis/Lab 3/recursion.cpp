#include <iostream>

// C   - total capacity
// n   - number of items
// w[] - array of weights
// p[] - array of profits
int P(int C, int n, int w[], int p[])
{
    // Base case
    if (C == 0)
        return 0;

    // keep track of profits of subproblem + p[i], i being subproblem item's index
    int sol[n];

    // Get profits for taking item 0 to n for all branches
    for (int i = 0; i < n; i++)
    {
        if (C >= w[i])
            sol[i] = P(C - w[i], n, w, p) + p[i];
        else
            sol[i] = 0; // Not enough space to pack item i
    }

    // Finds branch with highest profit
    int max = sol[0];
    for (int i = 1; i < n; i++)
    {
        if (sol[i] > max)
            max = sol[i];
    }
    return max;
}

int main()
{
    int w[3] = {4, 6, 8};
    int p[3] = {7, 6, 9};
    std::cout << "Recursive profit: " << P(14, 3, w, p) << std::endl;
}