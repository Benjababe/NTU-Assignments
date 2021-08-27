import java.util.Scanner;

public class Strings implements Comparable<Strings> {
    private String str;

    public Strings(String str) {
        this.str = str;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("\nHow many strings do you want to sort? ");
        int size = sc.nextInt();

        Strings[] strList = new Strings[size];
        System.out.println("\nEnter the numbers...");

        for (int i = 0; i < size; i++) {
            String str = sc.next();
            strList[i] = new Strings(str);
        }

        Sorting.insertionSort(strList);
        System.out.println("\nYour strings in sorted order...");

        for (int i = 0; i < size; i++) {
            System.out.print(strList[i].getString() + " ");
        }

        System.out.println();
        sc.close();
    }

    public String getString() {
        return this.str;
    }

    public int compareTo(Strings s2) {
        String tmp1 = this.str, tmp2 = s2.getString();

        // while first characters are equal, go to next char
        // ie if 2 string were "appleman" and "applebees",
        // they would compare at the 'm' and 'b' chars, skipping "apple"
        while (tmp1.length() > 0 && tmp2.length() > 0 && tmp1.charAt(0) == tmp2.charAt(0)) {
            tmp1 = tmp1.substring(1);
            tmp2 = tmp2.substring(1);
        }

        // if all chars match (same string)
        if (tmp1.length() == 0 && tmp2.length() == 0)
            return 0;

        // tmp2 is a substring of tmp1 eg. "Hell" & "Hello"
        // the longer string would be the "greater" value
        else if (tmp1.length() != 0 && tmp2.length() == 0)
            return 1;

        // tmp1 is a substring of tmp2
        else if (tmp1.length() == 0 && tmp2.length() != 0)
            return -1;

        // basic check of first char
        if (tmp1.charAt(0) < tmp2.charAt(0))
            return -1;

        else
            return 1;
    }
}
