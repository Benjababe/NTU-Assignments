class Q3_BubbleArray {
    int[] array;

    public Q3_BubbleArray() {

    }

    public Q3_BubbleArray(int size) {
        this.array = new int[size];
    }

    public void setSize(int size) {
        this.array = new int[size];
    }

    public void printArray() {
        System.out.println("\n\nFinally sorted array is: ");
        for (int i = 0; i < this.array.length; i++) {
            System.out.format("%d ", this.array[i]);
        }
    }

    public void insert(int index, int num) {
        this.array[index] = num;
    }

    public void sort() {
        int tmp;

        for (int i = 0; i < this.array.length - 1; i++) {
            for (int j = 0; j < this.array.length - i - 1; j++) {
                if (this.array[j] > this.array[j + 1]) {
                    tmp = this.array[j];
                    this.array[j] = this.array[j + 1];
                    this.array[j + 1] = tmp;
                }
            }
        }
    }
}