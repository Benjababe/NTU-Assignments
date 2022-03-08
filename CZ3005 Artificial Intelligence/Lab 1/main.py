from timeit import timeit
from misc import PathInfo, ENERGY_BUDGET, load_json_files
import task1
import task2
import task3

# no. of samples for task performance comparison
PERF_SAMPLES = 5000

# no. of samples for h(n) scaling comparison
SCALE_SAMPLES = 5000

# max value of gamma for h(n) scaling
GAMMA_LIMIT = 6

# value to increment gamma *10
GAMMA_INCREMENT = 2


def main():
    coord, cost, dist, g = load_json_files()

    # basic path finding output
    run_task_1(dist, g)
    run_task_2(cost, dist, g)
    run_task_3(coord, cost, dist, g)

    print("Everything from here may take some time to execute\n")

    # compare path finding performance between all 3 tasks
    # focus mainly on task 2 vs task 3
    perf_test_task_1(dist, g)
    perf_test_task_2(cost, dist, g)
    perf_test_task_3(coord, cost, dist, g)

    # leave this to run overnight la. takes forever one
    # finds out how scaling the h(n) affects the path distance and computation time
    scale_test_task_3(coord, cost, dist, g)
# end_main


def run_task_1(dist: dict, g: dict) -> None:
    path1 = task1.ucs('1', '50', dist, g)
    print_path("Task 1", path1)
# end_run_task_1


def run_task_2(cost: dict, dist: dict, g: dict) -> None:
    path2 = task2.ucs('1', '50', ENERGY_BUDGET, cost, dist, g)
    print_path("Task 2", path2)
# end_run_task_2


def run_task_3(coord: dict, cost: dict, dist: dict, g: dict) -> None:
    path3 = task3.astar('1', '50', ENERGY_BUDGET, coord, cost, dist, g)
    print_path("Task 3", path3)
# end_run_task_2


def perf_test_task_1(dist: dict, g: dict) -> None:
    avg_time = timeit(lambda: task1.ucs('1', '50', dist, g),
                      setup="import task1", number=PERF_SAMPLES) / PERF_SAMPLES * 1000

    msg = f"(Task 1) Average time taken: {avg_time:.2f} ms from {PERF_SAMPLES} samples"
    print(msg)
# end_perf_test_task_1


def perf_test_task_2(cost: dict, dist: dict, g: dict) -> None:
    avg_time = timeit(lambda: task2.ucs('1', '50', ENERGY_BUDGET, cost, dist, g),
                      setup="import task2", number=PERF_SAMPLES) / PERF_SAMPLES * 1000

    msg = f"(Task 2) Average time taken: {avg_time:.2f} ms from {PERF_SAMPLES} samples"
    print(msg)
# end_perf_test_task_2


def perf_test_task_3(coord: dict, cost: dict, dist: dict, g: dict) -> None:
    avg_time = timeit(lambda: task3.astar('1', '50', ENERGY_BUDGET, coord, cost, dist, g, gamma=1),
                      setup="import task3", number=PERF_SAMPLES) / PERF_SAMPLES * 1000

    msg = f"(Task 3) Average time taken: {avg_time:.2f} ms from {PERF_SAMPLES} samples"
    print(msg)
# end_perf_test_task_3


def scale_test_task_3(coord: dict, cost: dict, dist: dict, g: dict) -> None:
    for i in range(0, GAMMA_LIMIT*10 + 1, GAMMA_INCREMENT):
        gamma = i / 10

        for _ in range(SCALE_SAMPLES + 1):
            avg_time = timeit(lambda: task3.astar('1', '50', ENERGY_BUDGET, coord, cost, dist, g, gamma=gamma),
                              setup="import task3", number=PERF_SAMPLES) / SCALE_SAMPLES * 1000

            path = task3.astar('1', '50', ENERGY_BUDGET,
                               coord, cost, dist, g, gamma=gamma)

        msg = f"For gamma: {gamma}, avg time taken: {avg_time:.2f} ms, distance: {path.dist:.2f}"
        print(msg)
# end_scale_test_task_3


def print_path(label: str, path_info: PathInfo) -> None:
    print(label)
    print(f"Shortest path: {path_info.path}")
    print(f"Shortest distance: {path_info.dist}")
    print(f"Total energy cost: {path_info.energy}\n")
# end_print_path


if __name__ == "__main__":
    main()
