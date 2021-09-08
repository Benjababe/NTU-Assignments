#include <iostream>
#include <string>

#include "animalClass.h"
#include "childAnimal.h"

using namespace std;

int main()
{
    Mammal zoo[10];

    int input = -1, zooCount = 0;

    string name, owner = "Jerry";
    COLOR col = Brown;

    while (input != 0 && input != 5)
    {
        cout << "Select the animal to send to the Ani:\n"
             << "(1) Dog (2) Cat (3) Lion (4) Move all animals (5) Quit\n: ";
        cin >> input;

        // for simplicity's sake, we only ask for name.
        // color and owner will be default to brown and Jerry
        if (input >= 1 && input <= 3)
        {
            cout << "Enter name of the animal: ";
            cin >> name;
        }

        switch (input)
        {
        case 1:
            zoo[zooCount++] = Dog(name, col, owner);
            break;

        case 2:
            zoo[zooCount++] = Cat(name, col);
            break;

        case 3:
            zoo[zooCount++] = Lion(name, col);
            break;

        case 4:
            for (int i = 0; i < zooCount; i++)
            {
                zoo[i].move();
                zoo[i].speak();
                zoo[i].eat();
                cout << "\n";
            }
            break;

        case 5:
            break;

        default:
            break;
        }
    }

    return 0;
}
