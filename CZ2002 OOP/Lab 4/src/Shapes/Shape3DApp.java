import java.util.Scanner;

public class Shape3DApp {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter total number of shapes: ");
        int shapeNum = sc.nextInt();
        ThreeDeeShape[] shapes = new ThreeDeeShape[shapeNum];

        for (int i = 0; i < shapeNum; i++) {
            System.out.print("Choose a shape:\n1.Sphere\n2.Pyramid\n3.Cuboid\n:");
            int width, height, radius, base, length, shape = sc.nextInt();

            switch (shape) {
                case 1:
                    Sphere sphere = new Sphere();
                    System.out.print("Enter the radius of the sphere: ");
                    radius = sc.nextInt();
                    sphere.setRadius(radius);
                    shapes[i] = sphere;
                    break;

                case 2:
                    Pyramid pyr = new Pyramid();
                    System.out.print("Enter the base length of the square pyramid: ");
                    base = sc.nextInt();
                    System.out.print("Enter the height of the square pyramid: ");
                    height = sc.nextInt();
                    pyr.setDimensions(base, height);
                    shapes[i] = pyr;
                    break;

                case 3:
                    Cuboid cuboid = new Cuboid();
                    System.out.print("Enter the length of the cuboid: ");
                    length = sc.nextInt();
                    System.out.print("Enter the width of the cuboid: ");
                    width = sc.nextInt();
                    System.out.print("Enter the height of the cuboid: ");
                    height = sc.nextInt();
                    cuboid.setDimensions(length, width, height);
                    shapes[i] = cuboid;
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
            // consider overlapping shapes as well
            // subtract from both current and previous shapes as that
            // area is now not included
            if (i > 0) {
                // get smaller area of previous shape's top or current shape's bottom
                // we do this because previous shape might be pyramid/sphere with top area of 0
                // in that case, there isn't any overlap
                double area = Math.min(shapes[i - 1].getTopArea(), shapes[i].getBottomArea());
                totalArea -= 2 * area;
            }
        }

        System.out.format("Total area of shapes is %.2f\n", totalArea);
        sc.close();
    }
}
