#include <iostream>
#include <string>
using namespace std;

enum COLOR
{
    Green,
    Blue,
    White,
    Black,
    Brown
};

class Animal
{
public:
    Animal() : _name("unknown"), _color(Green)
    {
        cout << "Constructing Animal object " << _name << endl;
    }
    Animal(string n, COLOR c)
    {
        string colors[5] = {"green", "blue", "white", "black", "brown"};
        _name = n;
        _color = c;
        cout << "Constructing animal " << _name << " with color " << colors[c] << endl;
    }
    ~Animal()
    {
        cout << "Destructing Animal object named " << _name << endl;
    }
    void speak()
    {
        cout << "Animal speaks " << endl;
    }
    virtual void move() = 0;

protected:
    string _name;
    COLOR _color;
};

class Mammal : public Animal
{
public:
    Mammal(string n, COLOR c) : Animal(n, c)
    {
    }
    void eat() const
    {
        cout << _name << " the mammal eats" << endl;
    }
    void move()
    {
        cout << _name << " the mammal moves" << endl;
    }
};

class Dog : public Mammal
{
public:
    Dog(string n, COLOR c, string o) : Mammal(n, c)
    {
        _owner = o;
        cout << "Owner of " << _name << " is " << _owner << endl;
    }
    void speak()
    {
        cout << _name << " the dog woofs" << endl;
    }
    void move() override
    {
        cout << _name << " the dog moved" << endl;
    }

protected:
    string _owner;
};

int main()
{
    // unable to declare Animal since it's purely abstract now
    //Animal a("Frog", Green);
    //a.speak();

    Mammal m("Elephant", White);
    m.eat();
    m.move();

    cout << endl;

    Dog d("Doggie", Black, "Bob");
    d.eat();
    d.speak();
    d.move();

    cout << endl;

    Dog dogi("Lassie", White, "Andy");
    Mammal *aniPtr = &dogi;
    Mammal &aniRef = dogi;
    Mammal aniVal = dogi;

    aniPtr->speak();
    aniRef.speak();
    aniVal.speak();

    cout << "\nProgram exiting ... " << endl;
    return 0;
}
