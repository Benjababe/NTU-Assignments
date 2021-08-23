public class Circle {
    private double radius; // radius of circle
    private static final double PI = 3.14159;

    // constructor
    public Circle(double rad) {
        this.radius = rad;
    }

    // mutator method – set radius
    public void setRadius(double rad) {
        this.radius = rad;
    }

    // accessor method – get radius
    public double getRadius() {
        return this.radius;
    }

    // calculate area
    public double area() {
        return this.radius * this.radius * PI;
    }

    // calculate circumference
    public double circumference() {
        return 2 * this.radius * PI;
    }

    // print area
    public void printArea() {
        System.out.format("Area is %f units squared\n", this.radius * this.radius * PI);
    }

    // print circumference
    public void printCircumference() {
        System.out.format("Area is %f units long\n", 2 * this.radius * PI);
    }
}
