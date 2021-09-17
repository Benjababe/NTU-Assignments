import random
import time

key_comparisons = 0
NUM_TRIALS = 5000
ARR_SIZE = 2**14
filename = f"./compare_sorts_{NUM_TRIALS}.txt"
results = {
    "custom_sort": [],
    "merge_sort": []
}


def insertion_sort(arr, n, m):
    global key_comparisons

    for i in range(n+1, m+1):
        for j in range(i, n, -1):
            key_comparisons += 1
            if (arr[j] < arr[j-1]):
                temp = arr[j]
                arr[j] = arr[j-1]
                arr[j-1] = temp
            else:
                break
# end_insertion_sort


# separate list approach
def merge_sort_sep(arr):
    global key_comparisons
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr)//2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        merge_sort_sep(L)

        # Sorting the second half
        merge_sort_sep(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            key_comparisons += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            key_comparisons += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            key_comparisons += 1
# end_merge_sort_sep


# custom sort splitting the list up instead of inplace swaps
def custom_sort_sep(arr, S):
    global key_comparisons
    if len(arr) <= S:
        insertion_sort(arr, 0, len(arr) - 1)

    elif len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr)//2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        custom_sort_sep(L, S)

        # Sorting the second half
        custom_sort_sep(R, S)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            key_comparisons += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            key_comparisons += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            key_comparisons += 1
# end_custom_sort_sep


# generate randomised array of length len without any repeats
def gen_rand_arr(len):
    arr = list(range(1, len + 1))
    random.shuffle(arr)
    return arr


# trials array of sizes 6-14 on customsort with S=31 and compares with regular mergesort
def trial_n(type, S=15):
    global key_comparisons, NUM_TRIALS
    # loop from 6-14
    for arr_len in range(6, 15):
    #for arr_len in range(12, 13):
        time_taken_arr = []
        key_comp_arr = []

        for i in range(NUM_TRIALS):
            # generate array of length 2**array_len
            arr = gen_rand_arr(2**arr_len)
            key_comparisons = 0
            start = time.perf_counter_ns()

            if type == "custom_sort":
                custom_sort_sep(arr, S)

            elif type == "merge_sort":
                merge_sort_sep(arr)

            time_taken_ms = (time.perf_counter_ns() - start) / 10**6
            time_taken_arr.append(time_taken_ms)
            key_comp_arr.append(key_comparisons)

        avg_time_taken_ms = round(sum(time_taken_arr) / len(time_taken_arr), 2)
        avg_key_comparisons = round(sum(key_comp_arr) / len(key_comp_arr))
        tag = f"{type}, S={S}" if type == "custom_sort" else type
        #out = f"[{tag}] For array size={2**arr_len}:  \t{avg_time_taken_ms}ms,\taverage key comparisons: {avg_key_comparisons:15}"
        out = f"{2**arr_len}\t{S}\t{avg_time_taken_ms}\t{avg_key_comparisons}"
        print(out)

        with open(filename, "a") as f:
            f.write(out + "\n")
            f.close()
# end_trial_n


if __name__ == "__main__":
    '''
    # max value of S to increment until
    MAX_S = 50
    out = f"Average time of {NUM_TRIALS} time trials for sorting array of size {ARR_SIZE}:"
    print(out)

    with open(filename, "w") as f:
        f.write(out + "\n")
        f.close()

    # test S values from 2 - MAX_S
    for S in range(2, MAX_S+1):
        trial_n("custom_sort", S)

    # trials merge sort once to compare with all S value sorts
    trial_n("merge_sort")

    '''
    with open(filename, "w") as f:
        f.write("Lab 1 output:\n")
        print("Array Length\tS\tCPU Time\tKey Comparisons")
        f.write("Array Length\tS\tCPU Time\tKey Comparisons")
        f.close()

    trial_n("custom_sort", 32)
    trial_n("merge_sort")
