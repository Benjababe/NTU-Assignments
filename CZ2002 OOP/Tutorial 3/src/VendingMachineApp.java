import java.util.Scanner;

public class VendingMachineApp {
    public static void main(String[] args) {
        VendingMachine vm = new VendingMachine();
        Scanner scanner = new Scanner(System.in);

        System.out.println("====== Vending Machine ======");
        System.out.println("|1. Buy Beer ($3.00)        |");
        System.out.println("|2. Buy Coke ($1.00)        |");
        System.out.println("|3. Buy Green Tea ($5.00)   |");
        System.out.println("|============================");
        System.out.println("Please enter selection:");

        int drink = Integer.parseInt(scanner.nextLine());
        vm.selectDrink(drink);

        System.out.println("Please insert coins:");
        System.out.println("========== Coins Input ===========");
        System.out.println("|Enter 'Q' for ten cents input   |");
        System.out.println("|Enter 'T' for twenty cents input|");
        System.out.println("|Enter 'F' for fifty cents input |");
        System.out.println("|Enter 'N' for a dollar input    |");
        System.out.println("==================================");

        double remainder;
        do {
            String coinInput = scanner.nextLine().toUpperCase();
            remainder = vm.insertCoins(coinInput);
        } while (remainder > 0);

        vm.checkChange();
        scanner.close();
    }
}
