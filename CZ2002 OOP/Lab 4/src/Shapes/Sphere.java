public class Sphere extends ThreeDeeShape {
    double radius;

    public void setRadius(double radius) {
        this.radius = radius;
        this.setTopArea(0);
        this.setBottomArea(0);
    }

    public double getArea() {
        return 4 * this.radius * this.radius * Math.PI;
    }
}
