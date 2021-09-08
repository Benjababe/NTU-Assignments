#include <string>

using namespace std;

#ifndef A_CLASS
#define A_CLASS

enum COLOR
{
    Green,
    Blue,
    White,
    Black,
    Brown
};

class Animal;
class Animal
{
public:
    Animal();
    Animal(string n, COLOR c);
    ~Animal();
    void speak();
    virtual void move() = 0;

protected:
    string _name;
    COLOR _color;
};

class Mammal;
class Mammal : public Animal
{
public:
    Mammal();
    Mammal(string n, COLOR c);
    void eat() const;
    virtual void move();
};

#endif