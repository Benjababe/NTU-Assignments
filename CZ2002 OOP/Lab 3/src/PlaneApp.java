import java.util.Scanner;

public class PlaneApp {
    public static void main(String[] args) {
        System.out.println("(1) Show number of empty seats");
        System.out.println("(2) Show the list of empty seats");
        System.out.println("(3) Show the list of seat assignments by seat ID");
        System.out.println("(4) Show the list of seat assignments by customer ID");
        System.out.println("(5) Assign a customer to a seat");
        System.out.println("(6) Remove a seat assignment");
        System.out.println("(7) Exit");

        Plane plane = new Plane();
        int seatId, cust_id;

        Scanner sc = new Scanner(System.in);
        System.out.print("Please enter the number of your choice: ");
        String input = sc.next().trim();

        // ends loop on "7" as choice
        while (!input.equals("7")) {
            switch (input) {
                case "1":
                    plane.showNumEmptySeats();
                    break;

                case "2":
                    plane.showEmptySeats();
                    break;

                case "3":
                    plane.showAssignedSeats(true);
                    break;

                case "4":
                    plane.showAssignedSeats(false);
                    break;

                case "5":
                    System.out.print("Assigning seat...\nPlease enter SeatID: ");
                    seatId = sc.nextInt();
                    System.out.print("Please enter Customer ID: ");
                    cust_id = sc.nextInt();
                    plane.assignSeat(seatId, cust_id);
                    break;

                case "6":
                    System.out.print("Please enter SeatID to unassign customer from: ");
                    seatId = sc.nextInt();
                    plane.unAssignSeat(seatId);
                    break;
            }
            System.out.print("\nEnter the number of your choice: ");
            input = sc.next().trim();
        }

        sc.close();
    }
}
