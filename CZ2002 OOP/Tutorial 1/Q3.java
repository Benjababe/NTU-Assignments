import java.util.Scanner;

public class Q3 {
    public static void main(String[] args) {
        System.out.println("\n\nEnter number of Integer elements to be sorted:");
        Scanner sc = new Scanner(System.in);
        int n = Integer.parseInt(sc.nextLine());

        Q3_BubbleArray bubbleArray = new Q3_BubbleArray();
        bubbleArray.setSize(n);

        for (int i = 0; i < n; i++) {
            System.out.format("\n\nEnter integer value for element no. %d: ", i + 1);
            int num = Integer.parseInt(sc.nextLine());
            bubbleArray.insert(i, num);
        }

        sc.close();

        bubbleArray.sort();
        bubbleArray.printArray();
    }
}
