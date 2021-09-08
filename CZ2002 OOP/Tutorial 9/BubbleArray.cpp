#include <iostream>

#include "BubbleArray.h"

using namespace std;

BubbleArray::BubbleArray()
{
}

BubbleArray::~BubbleArray()
{
}

void BubbleArray::setSize(int n)
{
    _i = 0;
    _n = n;
}

void BubbleArray::printArray()
{
    cout << "Finally sorted array is: " << endl;
    for (int i = 0; i < _n; i++)
    {
        cout << _array[i] << " ";
    }
    cout << endl;
}

void BubbleArray::insert(int item)
{
    _array[_i++] = item;
}

void BubbleArray::sort()
{
    int tmp;
    for (int i = _n - 2; i >= 0; i--)
    {
        for (int j = 0; j <= i; j++)
        {
            if (_array[j] > _array[j + 1])
            {
                tmp = _array[j];
                _array[j] = _array[j + 1];
                _array[j + 1] = tmp;
            }
        }
    }
}

int main()
{
    int n;
    cout << "Enter number of integer elements to be sorted: ";
    cin >> n;
    BubbleArray bubbleArray;
    bubbleArray.setSize(n);

    for (int i = 0; i < n; i++)
    {
        int item;
        cout << "Enter integer value for element no." << (i + 1) << ": ";
        cin >> item;
        bubbleArray.insert(item);
    }

    bubbleArray.sort();
    bubbleArray.printArray();
}