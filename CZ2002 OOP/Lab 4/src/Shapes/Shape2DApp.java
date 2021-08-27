import java.util.Scanner;

public class Shape2DApp {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter total number of shapes: ");
        int shapeNum = sc.nextInt();
        Shape[] shapes = new Shape[shapeNum];

        for (int i = 0; i < shapeNum; i++) {
            System.out.print("Choose a shape:\n1.Square\n2.Rectangle\n3.Circle\n4.Triangle\n:");
            int width, height, side, radius, base, shape = sc.nextInt();

            switch (shape) {
                case 1:
                    Square sq = new Square();
                    System.out.print("Enter the length of side of the square: ");
                    side = sc.nextInt();
                    sq.setSide(side);
                    shapes[i] = sq;
                    break;

                case 2:
                    Rectangle rect = new Rectangle();
                    System.out.print("Enter the width of the rectangle: ");
                    width = sc.nextInt();
                    rect.setWidth(width);
                    System.out.print("Enter the height of the rectangle: ");
                    height = sc.nextInt();
                    rect.setHeight(height);
                    shapes[i] = rect;
                    break;

                case 3:
                    Circle c = new Circle();
                    System.out.print("Enter the radius of the circle: ");
                    radius = sc.nextInt();
                    c.setRadius(radius);
                    shapes[i] = c;
                    break;

                case 4:
                    Triangle tri = new Triangle();
                    System.out.print("Enter the base of the triangle: ");
                    base = sc.nextInt();
                    tri.setBase(base);
                    System.out.print("Enter the height of the triangle: ");
                    height = sc.nextInt();
                    tri.setHeight(height);
                    shapes[i] = tri;
                    break;

                default:
                    System.out.println("Invalid choice, try again...");
                    i--;
                    break;
            }
        }

        double totalArea = 0;

        for (int i = 0; i < shapeNum; i++) {
            totalArea += shapes[i].getArea();
        }

        System.out.format("Total area of shapes is %.2f\n", totalArea);
        sc.close();
    }
}
