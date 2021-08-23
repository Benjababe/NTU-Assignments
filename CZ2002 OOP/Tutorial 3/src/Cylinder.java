public class Cylinder extends Circle {
    int height;

    public Cylinder() {
        this.height = 0;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getHeight() {
        return this.height;
    }

    public double area() {
        return (2 * this.radius * this.height * Math.PI) + (2 * this.radius * this.radius * Math.PI);
    }

    public double volume() {
        return this.radius * this.radius * this.height * Math.PI;
    }

    public String toString() {
        return String.format("[ %d, %d, %d, %d]", this.x, this.y, this.radius, this.height);
    }
}
