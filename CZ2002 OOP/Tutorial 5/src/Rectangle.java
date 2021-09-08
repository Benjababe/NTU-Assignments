public class Rectangle extends Polygon {
    public Rectangle(float width, float height) {
        super("Rectangle", width, height);
        this.setPolytype(KindofPolygon.POLY_RECT);
    }

    @Override
    public float calArea() {
        return this.width * this.height;
    }

    public void printArea() {
        float area = this.calArea();
        System.out.println("Area of " + name + " is " + area + " units^2");
    }

    public static void printArea(float width, float height) {
        float area = width * height;
        System.out.println("Area of rectangle is " + area + " units^2");
    }
}
