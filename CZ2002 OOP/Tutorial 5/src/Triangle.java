public class Triangle extends Polygon {
    public Triangle(float width, float height) {
        super("Triangle", width, height);
        this.setPolytype(KindofPolygon.POLY_TRIANG);
    }

    @Override
    public float calArea() {
        return (this.width * this.height) / 2;
    }

    public void printArea() {
        float area = this.calArea();
        System.out.println("Area of " + name + " is " + area + " units^2");
    }

    public static void printArea(float width, float height) {
        float area = (width * height) / 2;
        System.out.println("Area of triangle is " + area + " units^2");
    }
}
