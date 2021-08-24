import java.util.Scanner;

public class P2 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter salary: $");
        double salary = Double.parseDouble(sc.nextLine());
        System.out.print("Enter merit pts: ");
        int merit = Integer.parseInt(sc.nextLine());

        if (salary >= 500 && salary <= 649) {
            if (salary >= 600 && merit >= 10)
                System.out.println("Person is in Grade B");
            else
                System.out.println("Person is in Grade C");
        }

        else if (salary >= 600 && salary <= 799) {
            if (salary >= 700 && merit >= 20)
                System.out.println("Person is in Grade A");
            else
                System.out.println("Person is in Grade B");
        }

        else if (salary >= 800 && salary <= 899)
            System.out.println("Person is in Grade A");

        sc.close();
    }
}
