import java.util.Scanner;

public class CircleApp {
    public static void main(String[] args) {
        Circle circle = null;
        double radius = 0;

        printBoard();
        boolean run = true;

        while (run) {
            System.out.println("Choose option (1-3):");

            Scanner scanner = new Scanner(System.in);
            String selection = scanner.nextLine().trim();

            switch (selection) {
                case "1":
                    radius = getRadius(scanner);
                    circle = new Circle(radius);
                    System.out.println("A new circle is created");
                    break;

                case "2":
                    double area = circle.area();
                    System.out.format("Area of circle\nRadius: %.4f\nArea: %.4f\n", radius, area);
                    break;

                case "3":
                    double circumference = circle.circumference();
                    System.out.format("Circumference of circle\nRadius: %.4f\nCircumference: %.4f\n", radius,
                            circumference);
                    break;

                case "4":
                    System.out.println("Thank you!!");
                    run = false;
                    break;
            }

            scanner.close();
        }
    }

    private static void printBoard() {
        System.out.println("==== Circle Computation =====");
        System.out.println("|1. Create a new circle     |");
        System.out.println("|2. Print Area              |");
        System.out.println("|3. Print circumference     |");
        System.out.println("|4. Quit                    |");
        System.out.println("=============================");
    }

    private static double getRadius(Scanner scanner) {
        System.out.println("Enter the radius to compute the area and circumference");
        String radiusIn = scanner.nextLine();
        double radius = Double.parseDouble(radiusIn);
        return radius;
    }
}