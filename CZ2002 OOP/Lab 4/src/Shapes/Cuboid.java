public class Cuboid extends ThreeDeeShape {
    Rectangle wl, wh, hl;
    double length;

    public void setDimensions(double length, double width, double height) {
        this.length = length;
        this.width = width;
        this.height = height;

        wl = new Rectangle();
        wl.setHeight(length);
        wl.setWidth(width);
        this.setBottomArea(wl.getArea());
        this.setTopArea(wl.getArea());

        wh = new Rectangle();
        wh.setHeight(height);
        wh.setWidth(width);

        hl = new Rectangle();
        hl.setHeight(height);
        hl.setWidth(length);
    }

    // consists of 6 rectangles, 2 for every dimension pair
    public double getArea() {
        double area = 2 * wl.getArea() + 2 * wh.getArea() + 2 * hl.getArea();
        return area;
    }
}
