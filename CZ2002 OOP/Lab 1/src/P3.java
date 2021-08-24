import java.util.Scanner;

public class P3 {
    public static void main(String[] args) {
        final double USD_TO_SGD = 1.82;

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter starting value: $");
        int start = Integer.parseInt(sc.nextLine());

        System.out.print("Enter ending value: $");
        int end = Integer.parseInt(sc.nextLine());

        System.out.print("Enter increment: $");
        int increment = Integer.parseInt(sc.nextLine());

        sc.close();

        if (start > end) {
            System.out.println("Error: starting is larger than ending value");
            return;
        }

        if (increment <= 0) {
            System.out.println("Error: incrementing starting value by 0 or negative value");
            return;
        }

        // table 1, for loop
        System.out.println("\nTable 1");
        System.out.println("US$\t\tS$");
        System.out.println("--------------------");

        for (int count = start; count <= end; count += increment) {
            System.out.format("%d\t\t%.2f\n", count, count * USD_TO_SGD);
        }

        // table 2, while loop
        int count = start;
        System.out.println("\nTable 2");
        System.out.println("US$\t\tS$");
        System.out.println("--------------------");

        while (count <= end) {
            System.out.format("%d\t\t%.2f\n", count, count * USD_TO_SGD);
            count += increment;
        }

        // table 3, do while loop
        count = start;
        System.out.println("\nTable 3");
        System.out.println("US$\t\tS$");
        System.out.println("--------------------");

        do {
            System.out.format("%d\t\t%.2f\n", count, count * USD_TO_SGD);
            count += increment;
        } while (count <= end);
    }
}
