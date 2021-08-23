public class Circle extends Point {
    int radius;

    public Circle() {
        this.radius = 0;
    }

    public void setRadius(int radius) {
        this.radius = radius;
    }

    public int getRadius() {
        return this.radius;
    }

    public double area() {
        return this.radius * this.radius * Math.PI;
    }

    public String toString() {
        return String.format("[ %d, %d, %d ]", this.x, this.y, this.radius);
    }
}
