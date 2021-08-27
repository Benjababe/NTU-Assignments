public class Sorting {
	// -----------------------------------------------------------------
	// Sorts the specified array of objects using the selection
	// sort algorithm.
	// -----------------------------------------------------------------
	public static void selectionSort(Comparable[] list) {
		int min;
		Comparable temp;
		for (int index = 0; index < list.length - 1; index++) {
			min = index;
			for (int scan = index + 1; scan < list.length; scan++)
				if (list[scan].compareTo(list[min]) < 0)
					min = scan;
			// Swap the values
			temp = list[min];
			list[min] = list[index];
			list[index] = temp;
		}
	}

	// -----------------------------------------------------------------
	// Sorts the specified array of objects using the insertion
	// sort algorithm.
	// -----------------------------------------------------------------
	public static void insertionSort(Comparable[] list) {
		for (int index = 1; index < list.length; index++) {
			Comparable key = list[index];
			int position = index;
			// Shift larger values to the right
			while (position > 0 && key.compareTo(list[position - 1]) < 0) {
				list[position] = list[position - 1];
				position--;
			}
			list[position] = key;
		}
	}

	public static void insertionSortDesc(Comparable[] list) {
		// runs from 2nd last item to first item
		for (int i = list.length - 2; i >= 0; i--) {
			int pos = i;
			// runs from current item to last item
			for (int j = i + 1; j < list.length; j++) {
				if (list[pos].compareTo(list[j]) > 0) {
					Comparable tmp = list[pos];
					list[pos] = list[j];
					list[j] = tmp;
					pos++;
				}

				else
					break;
			}
		}
	}
}
//