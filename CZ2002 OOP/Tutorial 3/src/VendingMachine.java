import java.util.HashMap;

public class VendingMachine {
    Drink[] drinks;
    double sum, activePrice;
    int activeDrink;
    HashMap<String, Double> coinMap;

    // constructor
    public VendingMachine() {
        this.sum = 0;
        this.activePrice = 0;
        populateCoins();
        populateDrinks();
    }

    private void populateCoins() {
        this.coinMap = new HashMap<String, Double>();
        this.coinMap.put("Q", 0.10);
        this.coinMap.put("T", 0.20);
        this.coinMap.put("F", 0.50);
        this.coinMap.put("N", 1.00);
    }

    private void populateDrinks() {
        this.drinks = new Drink[3];
        this.drinks[0] = new Drink("Beer", 3.00);
        this.drinks[1] = new Drink("Coke", 1.00);
        this.drinks[2] = new Drink("Green Tea", 5.00);
    }

    // get the drink selection, and return the cost of the drink
    // added drink argument for which drink you selected
    public double selectDrink(int drink) {
        this.activeDrink = drink + 1;
        this.activePrice = this.drinks[drink - 1].getPrice();
        return this.activePrice;
    }

    // insert the coins and returns the amount left
    // changed coin value to coin type
    public double insertCoins(String coinInput) {
        if (this.activeDrink < 0) {
            System.out.println("Select a drink first!");
            return -1;
        }

        this.sum += (double) coinMap.get(coinInput);
        System.out.format("Coin inserted: %.2f\n", sum);
        return this.activePrice - this.sum;
    }

    // check the change and print the change on screen
    // removed arguments and use internal values instead
    public void checkChange() {
        if (this.activeDrink < 0) {
            System.out.println("Select a drink first!");
            return;
        }

        if (this.sum > this.activePrice) {
            System.out.format("Change: $ %.2f\n", (this.sum - this.activePrice));
            printReceipt();
        }
    }

    // print the receipt and collect the drink
    public void printReceipt() {
        this.sum = 0;
        this.activePrice = 0;
        this.activeDrink = -1;
        System.out.println("Please collect your drink\nThank You!!");
    }
}
