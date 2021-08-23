import java.util.Random;

public class Dice {
    int valueOfDice = 0;

    void setDiceValue() {
        Random random = new Random();
        while (this.valueOfDice == 0)
            this.valueOfDice = random.nextInt(6);
    }

    int getDiceValue() {
        return this.valueOfDice;
    }

    void printDiceValue() {
        System.out.format("Current Value is %d\n", this.valueOfDice);
    }
}
