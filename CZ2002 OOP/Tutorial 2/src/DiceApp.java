import java.util.Scanner;

public class DiceApp {
    public static void main(String[] args) {
        Dice[] dices = { new Dice(), new Dice() };
        Scanner scanner = new Scanner(System.in);

        System.out.println("Press <return> to roll the first dice");
        scanner.nextLine();
        dices[0].setDiceValue();
        dices[0].printDiceValue();

        System.out.println("Press <return> to roll the second dice");
        scanner.nextLine();
        dices[1].setDiceValue();
        dices[1].printDiceValue();

        System.out.format("Your total number is %d", (dices[0].getDiceValue() + dices[1].getDiceValue()));
        scanner.close();
    }
}
