#include <string>
#include <iostream>

#include "childAnimal.h"

using namespace std;

#ifdef C_CLASS
#define C_CLASS

Dog::Dog(string n, COLOR c, string o) : Mammal(n, c), _owner(o)
{
    cout << "Owner of " << _name << " is " << _owner << endl;
}

void Dog::speak()
{
    cout << _name << " the dog woofs" << endl;
}

void Dog::move()
{
    cout << _name << " the dog moved" << endl;
}

Cat::Cat(string n, COLOR c) : Mammal(n, c)
{
}

void Cat::move()
{
    cout << _name << " the cat moves" << endl;
}

void Cat::speak()
{
    cout << _name << " the cat meows" << endl;
}

Lion::Lion(string n, COLOR c) : Mammal(n, c) {}

void Lion::move()
{
    cout << _name << " the lion moves" << endl;
}

void Lion::speak()
{
    cout << _name << " the lion roars" << endl;
}

#endif