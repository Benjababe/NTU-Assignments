public abstract class Polygon {
    public enum KindofPolygon {
        POLY_PLAIN, POLY_RECT, POLY_TRIANG
    };

    protected String name;
    protected float width;
    protected float height;
    protected KindofPolygon polytype;

    public Polygon(String theName, float theWidth, float theHeight) {
        this.name = theName;
        this.width = theWidth;
        this.height = theHeight;
        this.polytype = KindofPolygon.POLY_PLAIN;
    }

    public KindofPolygon getPolytype() {
        return this.polytype;
    }

    public void setPolytype(KindofPolygon value) {
        this.polytype = value;
    }

    public String getName() {
        return this.name;
    }

    public abstract float calArea();

    public void printWidthHeight() {
        System.out.println("Width = " + this.width + " Height = " + this.height);
    }
}
