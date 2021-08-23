public class PowerFailureException extends Exception {
    String message;

    public PowerFailureException() {
        this.message = "Power Failure!";
    }

    public PowerFailureException(String message) {
        this.message = message;
    }

    public String getMessage() {
        return this.message;
    }
}
