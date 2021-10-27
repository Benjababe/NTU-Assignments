#include <string>
#include <iostream>

#include "animalClass.h"

using namespace std;

#ifdef A_CLASS
#define A_CLASS

Animal::Animal() : _name("unknown"), _color(Green)
{
    cout << "Constructing Animal object " << _name << endl;
}

Animal::Animal(string n, COLOR c) : _name(n), _color(c)
{
    string colors[5] = {"green", "blue", "white", "black", "brown"};
    cout << "Constructing animal " << _name << " with color " << colors[c] << endl;
}

Animal::~Animal()
{
    cout << "Destructing Animal object named " << _name << endl;
}

void Animal::speak()
{
    cout << "Animal speaks " << endl;
}

Mammal::Mammal()
{
}

Mammal::Mammal(string n, COLOR c) : Animal(n, c)
{
}

void Mammal::eat() const
{
    cout << _name << " the mammal eats" << endl;
}

void Mammal::move()
{
    cout << _name << " the mammal moves" << endl;
}

#endif //A_CLASS