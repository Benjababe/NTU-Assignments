public class Q12 {
    public static void main(String[] args) throws Exception {
        ClassF z = new ClassF();
        z.print(9); // f
        z.print(2, "Cx2002"); // a
        z.print("Object"); // e
        z.print("OODP", "Java"); // c
        // z.print("OODP", 2002);
        // last is error as ClassF only inherits from
        // Classes A, C and E

        // will print ClassD's method since it overrides C's
        ClassC c = new ClassD();
        c.print("Hello", "There");

        // will print ClassA's method as C is a subclass of A
        // and C will have A's methods by default
        ClassA a = new ClassC();
        a.print(1, "There");

        // a = new ClassF();
        // a.print("Hello", "There");
        // result in error as A has no superclasses and only
        // method for print takes an integer and string as arguments

        // c = new ClassD();
        // ClassE e = c;
        // result in error as ClassD and E are siblings with their own
        // unique properties

        a = new ClassF();
        a.print(12, "There");
        // a.print(88);
        // error as ClassA does not implement any of its children's methods

        a = new ClassC();
        // ClassG g = (ClassG) a;
        // g.print("Hello");
        // object a is actually a ClassC object but bounded to properties of A
        // casting error as ClassC might not hold all properties of G

        a = new ClassC();
        // ClassG g = (ClassG) a;
        // g.print("Hello", "There");
        // downcasting error again as above

        a = new ClassF();
        ClassC f = (ClassC) a;
        f.print(88, "There");
        // no casting error here as ClassF holds all properties of C
        // keep in mind that a is actually a ClassF object, not ClassA
    }
}

class ClassA {
    public void print(int x, String y) {
        System.out.println("ClassA's print method");
    }
}

class ClassB extends ClassA {
    public void print(int x) {
        System.out.println("ClassB's print method");
    }
}

// if print is abstract, ClassC has to be abstract as well
// and the print function must be defined in its subclass
/*
 * abstract class ClassC extends ClassA { public abstract void print(String x,
 * String y); }
 */

class ClassC extends ClassA {
    public void print(String x, String y) {
        System.out.println("ClassC's print method");
    }
}

class ClassD extends ClassC {
    // ClassD's print method overrides ClassC's by default
    public void print(String a, String b) {
        System.out.println("ClassD's print method");
    }
}

class ClassE extends ClassC {
    public void print(String x) {
        System.out.println("ClassE's print method");
    }

    // Implementing ClassC's method
    public void print(String x, String y) {
        System.out.println("ClassC's abstract print method");
    }
}

class ClassF extends ClassE {
    public void print(int x) {
        System.out.println("ClassF's print method");
    }
}

class ClassG extends ClassE {
    public void print(String x) {
        System.out.println("ClassG's print method");
    }
}
