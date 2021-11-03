import time
import compare_sorts

i_sort_times = []
m_sort_times = []

trial_times = 100000

# tries array sizes from 2-40 and compares the
# insertion sort and merge sort timing for each array size

# at the size where merge sort becomes faster than insertion sort
# is what we should choose as the optimal S value
# output will be written to finding_s.txt file
for arr_len in range(2, 41):    
    print(f"Trialing array size {arr_len}")
    ist = []
    mst = []

    # trials array of every length {trial_times} times
    for i in range(trial_times):
        arr1 = compare_sorts.gen_rand_arr(arr_len)
        arr2 = arr1.copy()

        # get insertion sort time in ns
        i_sort_start = time.perf_counter_ns()
        compare_sorts.insertion_sort(arr1, 0, arr_len - 1)
        i_sort_time = (time.perf_counter_ns() - i_sort_start)
        ist.append(i_sort_time)

        # get merge sort time in ns
        m_sort_start = time.perf_counter_ns()
        compare_sorts.merge_sort_sep(arr2)
        #compare_sorts.merge_sort(arr2, 0, arr_len - 1)
        m_sort_time = (time.perf_counter_ns() - m_sort_start)
        mst.append(m_sort_time)

    # appends averages of i_sort and m_sort times of all the trials
    i_sort_times.append(sum(ist) / len(ist))
    m_sort_times.append(sum(mst) / len(mst))

cols = ["Array Size", "Insertion", "Merge",
        "How much faster insertion is than merge (ns)"]

with open(f"find_optimal_s_{trial_times}.txt", "w") as f:    
    f.write(f"With {trial_times} trials for every array length:\n\n")
    f.write(f"{cols[0]:10}\t{cols[1]:10}\t{cols[2]:10}\t{cols[3]}\n")

    for i in range(len(i_sort_times)):
        i_time = i_sort_times[i]
        m_time = m_sort_times[i]
        f.write(f"{i+2:10}\t{i_time:10}\t{m_time:10}\t{m_time - i_time}\n")

    f.close()
