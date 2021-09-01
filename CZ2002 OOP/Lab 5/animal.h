#include <string>
#include <iostream>

using namespace std;

namespace Zoo
{
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
        Mammal() {}
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
}