public class Drink {
    String name;
    double price;

    public Drink(String name, double price) {
        this.name = name;
        this.price = Math.round(price * 100.0) / 100.0;
    }

    public String getName() {
        return this.name;
    }

    public double getPrice() {
        return this.price;
    }
}
