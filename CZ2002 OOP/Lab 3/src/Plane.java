public class Plane {
    private PlaneSeat[] seat = new PlaneSeat[12];
    private int numEmptySeat = 12;

    public Plane() {
        for (int i = 0; i < 12; i++) {
            seat[i] = new PlaneSeat(i + 1);
        }
    }

    private PlaneSeat[] sortSeats() {
        // create copy of seat array
        PlaneSeat[] tempSeats = new PlaneSeat[12];
        for (int i = 0; i < 12; i++) {
            tempSeats[i] = this.seat[i];
        }

        for (int i = 1; i < 12; i++) {
            for (int j = i - 1; j >= 0; j--) {
                if (tempSeats[j].getCustomerID() > tempSeats[j + 1].getCustomerID()) {
                    PlaneSeat tmp = tempSeats[j];
                    tempSeats[j] = tempSeats[j + 1];
                    tempSeats[j + 1] = tmp;
                }
            }
        }

        return tempSeats;
    }

    public void showNumEmptySeats() {
        System.out.format("There are %d empty seat(s)\n", this.numEmptySeat);
    }

    public void showEmptySeats() {
        System.out.println("The following seats are empty:");
        for (int i = 0; i < 12; i++) {
            if (!seat[i].isOccupied())
                System.out.format("SeatID %d\n", seat[i].getSeatID());
        }
    }

    public void showAssignedSeats(boolean bySeatId) {
        // assign arr to either ordered by seat id or customer id
        PlaneSeat[] arr = (bySeatId) ? this.seat : sortSeats();

        System.out.println("The seat assignments are as follow:");
        for (int i = 0; i < 12; i++) {
            if (arr[i].isOccupied())
                System.out.format("SeatID %d is assigned to CustomerID %d\n", arr[i].getSeatID(),
                        arr[i].getCustomerID());
        }
    }

    public void assignSeat(int seatId, int cust_id) {
        for (int i = 0; i < 12; i++) {
            if (this.seat[i].getSeatID() == seatId) {
                if (this.seat[i].isOccupied()) {
                    System.out.println("Error: Seat is occupied");
                    return;
                }
                this.seat[i].assign(cust_id);
                this.numEmptySeat--;
                System.out.println("Seat assigned!");
            }
        }
    }

    public void unAssignSeat(int seatId) {
        for (int i = 0; i < 12; i++) {
            if (this.seat[i].getSeatID() == seatId) {
                if (!this.seat[i].isOccupied()) {
                    System.out.println("Error: Seat is unoccupied");
                    return;
                }
                this.seat[i].unAssign();
                this.numEmptySeat++;
                System.out.println("Seat unassigned!");
            }
        }
    }
}
