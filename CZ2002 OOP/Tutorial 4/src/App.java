public class App {
    public static void main(String[] args) {
        int waitTime = 46;
        try {
            System.out.println("Try block entered");

            if (waitTime > 30)
                throw new PowerFailureException("Custom failure message here");

            System.out.println("Leaving try block");
        }

        catch (PowerFailureException e) {
            System.out.println("Exception: " + e.getMessage());
        }

        System.out.println("After catch block");
    }
}
