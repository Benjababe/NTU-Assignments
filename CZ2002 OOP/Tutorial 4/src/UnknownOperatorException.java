public class UnknownOperatorException extends Exception {
    String message;

    public UnknownOperatorException(String operator) {
        this.message = String.format("%s is an unknown operator", operator);
    }

    public String getMessage() {
        return this.message;
    }
}
