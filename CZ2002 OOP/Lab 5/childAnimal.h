#include <string>
#include <iostream>

using namespace std;

namespace Zoo
{
    class Dog : public Mammal
    {
    public:
        Dog(string n, Zoo::COLOR c, string o) : Mammal(n, c)
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

    class Cat : public Mammal
    {
    public:
        Cat(string n, Zoo::COLOR c) : Mammal(n, c) {}
        void move()
        {
            cout << _name << " the cat moves" << endl;
        }
        void speak()
        {
            cout << _name << " the cat meows" << endl;
        }
    };

    class Lion : public Mammal
    {
    public:
        Lion(string n, Zoo::COLOR c) : Mammal(n, c) {}
        void move()
        {
            cout << _name << " the lion moves" << endl;
        }
        void speak()
        {
            cout << _name << " the lion roars" << endl;
        }
    };
}