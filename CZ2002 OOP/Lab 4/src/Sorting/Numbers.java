import java.util.Scanner;

public class Numbers implements Comparable<Numbers> {
	private int num;

	public Numbers(int num) {
		this.num = num;
	}

	// --------------------------------------------
	// Reads in an array of integers, sorts them,
	// then prints them in sorted order.
	// --------------------------------------------
	public static void main(String[] args) {
		Numbers[] intList;
		int size;
		Scanner scan = new Scanner(System.in);
		System.out.print("\nHow many integers do you want to sort? ");
		size = scan.nextInt();

		intList = new Numbers[size];
		System.out.println("\nEnter the numbers...");

		for (int i = 0; i < size; i++) {
			int num = scan.nextInt();
			intList[i] = new Numbers(num);
		}

		Sorting.insertionSortDesc(intList);
		System.out.println("\nYour numbers in sorted order...");

		for (int i = 0; i < size; i++) {
			System.out.print(intList[i].getNum() + " ");
		}

		System.out.println();
		scan.close();
	}

	public int getNum() {
		return this.num;
	}

	public int compareTo(Numbers num2) {
		if (this.num < num2.getNum())
			return -1;
		else if (this.num > num2.getNum())
			return 1;
		else
			return 0;
	}
}