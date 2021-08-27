public class SalePerson implements Comparable<Object> {
    String firstName, lastName;
    int totalSales;

    public SalePerson(String firstName, String lastName, int totalSales) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.totalSales = totalSales;
    }

    public String toString() {
        return String.format("%s, %s, : %d", lastName, firstName, totalSales);
    }

    public boolean equals(Object o) {
        SalePerson other = (SalePerson) o;
        return this.firstName == other.firstName && this.lastName == other.lastName;
    }

    public int compareTo(Object o) {
        SalePerson other = (SalePerson) o;
        if (this.totalSales < other.totalSales)
            return -1;

        if (this.totalSales > other.totalSales)
            return 1;

        return this.lastName.compareTo(other.lastName);
    }
}
