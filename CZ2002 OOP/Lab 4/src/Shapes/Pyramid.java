public class Pyramid extends ThreeDeeShape {
    Square baseSquare;
    Triangle sideTriangle;

    public void setDimensions(double baseLen, double height) {
        this.width = baseLen;
        this.height = height;

        this.baseSquare = new Square();
        this.baseSquare.setSide(baseLen);
        this.setBottomArea(this.baseSquare.getArea());
        this.setTopArea(0);

        this.sideTriangle = new Triangle();
        sideTriangle.setBase(baseLen);

        // calculate slant of pyramid
        double h = Math.sqrt(Math.pow((baseLen / 2), 2) + height * height);
        sideTriangle.setHeight(h);
    }

    // pyramid has square base and 4 side triangles
    public double getArea() {
        return 4 * sideTriangle.getArea() + baseSquare.getArea();
    }
}
