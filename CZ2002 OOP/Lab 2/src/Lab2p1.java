import java.util.Random;
import java.util.Scanner;

public class Lab2p1 {
    private static Scanner sc;

    public static void main(String[] args) {
        int choice, m = 4, n = 121456789, digit = 1;
        sc = new Scanner(System.in);
        do {
            System.out.println("\nPerform the following methods:");
            System.out.println("1: multiplication test");
            System.out.println("2: quotient using division by subtraction");
            System.out.println("3: remainder using division by subtraction");
            System.out.println("4: count the number of digits");
            System.out.println("5: position of a digit");
            System.out.println("6: extract all odd digits");
            System.out.println("7: quit");
            choice = sc.nextInt();
            switch (choice) {
                case 1: /* add mulTest() call */
                    mulTest();
                    break;
                case 2: /* add divide() call */
                    int quo = divide(m, n);
                    System.out.format("%d / %d = %d", m, n, quo);
                    break;
                case 3: /* add modulus() call */
                    int mod = modulus(m, n);
                    System.out.format("%d %s %d = %d\n", m, "%", n, mod);
                    break;
                case 4: /* add countDigits() call */
                    int count = countDigits(n);
                    System.out.format("Digit count is %d\n", count);
                    break;
                case 5: /* add position() call */
                    int pos = position(n, digit);
                    System.out.format("Position of %d is %d", digit, pos);
                    break;
                case 6: /* add extractOddDigits() call */
                    long odd = extractOddDigits(n);
                    System.out.format("Odd digits are: %d", odd);
                    break;
                case 7:
                    System.out.println("Program terminating ….");
            }
        } while (choice < 7);
        sc.close();
    }

    public static void mulTest() {
        Random rand = new Random();
        int count = 0, num1, num2;

        // loop 5 questions
        for (int i = 0; i < 5; i++) {
            // rand.nextInt generates 0-8 and we add 1 to it for 1-9
            num1 = rand.nextInt(8) + 1;
            num2 = rand.nextInt(8) + 1;
            System.out.format("How much is %d times %d? ", num1, num2);
            int ans = sc.nextInt();

            if (ans == num1 * num2)
                count++;
        }

        System.out.format("%d answers out of 5 are correct.\n", count);
    }

    public static int divide(int m, int n) {
        int quotient = 0;

        while (m > n) {
            m -= n;
            quotient++;
        }

        return quotient;
    }

    public static int modulus(int m, int n) {
        while (m > n) {
            m -= n;
        }
        return m;
    }

    public static int countDigits(int n) {
        if (n <= 0) {
            System.out.println("Error: Argument passed is either 0 or negative");
            return 0;
        }
        int count = 0;
        while (n > 0) {
            n /= 10;
            count++;
        }
        return count;
    }

    public static int position(int n, int digit) {
        String s = Integer.toString(n);
        return s.lastIndexOf(Integer.toString(digit)) + 1;
    }

    public static long extractOddDigits(long n) {
        if (n <= 0) {
            System.out.println("Error: Argument passed is either 0 or negative");
            return -1;
        }

        String odd = "";

        while (n > 0) {
            // gets last digit of n
            long digit = n % 10;

            // if last digit is odd, prepend odd string
            if (digit % 2 == 1)
                odd = Long.toString(digit) + odd;

            // gets rid of last digit of n
            n /= 10;
        }

        // returns -1 if no odd digits
        return (odd == "") ? -1 : Long.parseLong(odd);
    }
}