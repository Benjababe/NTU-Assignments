import java.util.Scanner;

public class Calculator {
    double result;
    Scanner sc;

    public Calculator() {
        this.result = 0;
        this.sc = new Scanner(System.in);

        System.out.println("Calculator is on");
        System.out.format("result = %f\n", this.result);
    }

    public void run() {
        while (getOperator()) {
            System.out.format("updated result = %f\n", this.result);
        }
        printFinal();
    }

    private void printFinal() {
        System.out.format("Final result = %f\nEnd of Program", this.result);
    }

    private String getInput() {
        String input = sc.nextLine();
        return input;
    }

    private boolean getOperator() {
        try {
            String operator = getInput().toLowerCase();
            double num;
            switch (operator) {
                case "+":
                    num = getNumber();
                    add(num);
                    break;

                case "-":
                    num = getNumber();
                    subtract(num);
                    break;

                case "*":
                    num = getNumber();
                    multiply(num);
                    break;

                case "/":
                    num = getNumber();
                    divide(num);
                    break;

                case "q":
                    return false;

                default:
                    throw new UnknownOperatorException(operator);
            }
        }

        catch (UnknownOperatorException ex) {
            System.out.format("%s\nPlease re-enter:\n", ex.getMessage());
            getOperator();
        }
        return true;
    }

    private double getNumber() {
        String input = getInput();
        double num = Double.parseDouble(input);
        return num;
    }

    private void add(double num) {
        System.out.format("result + %f\n", num);
        this.result += num;
    }

    private void subtract(double num) {
        System.out.format("result - %f\n", num);
        this.result -= num;
    }

    private void multiply(double num) {
        System.out.format("result * %f\n", num);
        this.result *= num;
    }

    private void divide(double num) {
        System.out.format("result / %f\n", num);
        this.result /= num;
    }
}
