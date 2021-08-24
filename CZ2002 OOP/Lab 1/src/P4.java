import java.util.Scanner;

public class P4 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter height: ");
        int height = Integer.parseInt(sc.nextLine());
        sc.close();

        if (height <= 0) {
            System.out.println("Error: height is less than equals to 0");
            return;
        }

        String pattern[] = { "BB", "AA" };
        for (int i = 1; i <= height; i++) {
            for (int j = i; j > 0; j--) {
                System.out.format("%s", pattern[j % 2]);
            }
            System.out.print("\n");
        }
    }
}
