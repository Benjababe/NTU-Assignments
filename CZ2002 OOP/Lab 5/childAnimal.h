#include <string>
#include "animalClass.h"

using namespace std;

#ifndef C_CLASS
#define C_CLASS

class Dog : public Mammal
{
public:
    Dog();
    Dog(string n, COLOR c, string o);
    void speak();
    void move() override;

protected:
    string _owner;
};

class Cat : public Mammal
{
public:
    Cat();
    Cat(string n, COLOR c);
    void move();
    void speak();
};

class Lion : public Mammal
{
public:
    Lion();
    Lion(string n, COLOR c);
    void move();
    void speak();
};

#endif //C_CLASS