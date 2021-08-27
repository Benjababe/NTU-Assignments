public class Triangle extends Shape {
    public void setBase(double base) {
        this.width = base;
    }

    public double getArea() {
        return this.height * this.width * 0.5;
    }
}
