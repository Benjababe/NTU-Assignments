public class Square extends Shape {
    public void setSide(double side) {
        this.height = side;
        this.width = side;
    }

    public double getArea() {
        return this.height * this.width;
    }
}
