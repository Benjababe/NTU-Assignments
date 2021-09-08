public class TestPolygon {
    public static void main(String[] args) {
        Rectangle r = new Rectangle(10, 5);
        Triangle t = new Triangle(10, 5);

        r.printArea();
        t.printArea();

        Rectangle.printArea(10, 5);
        Triangle.printArea(10, 5);
    }
}
