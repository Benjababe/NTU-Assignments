import time
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


def run_task_1(dist: dict, g: dict, printout: bool = True) -> None:
    path1 = task1.ucs('1', '50', dist, g)
    if printout:
        print_path("Task 1", path1)
# end_run_task_1


def run_task_2(cost: dict, dist: dict, g: dict, printout: bool = True) -> None:
    path2 = task2.ucs('1', '50', ENERGY_BUDGET, cost, dist, g)
    if printout:
        print_path("Task 2", path2)
# end_run_task_2


def run_task_3(coord: dict, cost: dict, dist: dict, g: dict, printout: bool = True) -> None:
    path3 = task3.astar('1', '50', ENERGY_BUDGET, coord, cost, dist, g)
    if printout:
        print_path("Task 3", path3)
# end_run_task_2


def perf_test_task_1(dist: dict, g: dict) -> None:
    total_time = 0

    for _ in range(PERF_SAMPLES + 1):
        start_time = time.perf_counter()
        task1.ucs('1', '50', dist, g)
        total_time += (time.perf_counter() - start_time)

    total_time *= 1000 / SCALE_SAMPLES
    total_time = round(total_time, 2)
    print(
        f"(Task 3) Average time taken: {total_time} ms from {PERF_SAMPLES} samples")
# end_perf_test_task_1


def perf_test_task_2(cost: dict, dist: dict, g: dict) -> None:
    total_time = 0

    for _ in range(PERF_SAMPLES + 1):
        start_time = time.perf_counter()
        task2.ucs('1', '50', ENERGY_BUDGET, cost, dist, g)
        total_time += (time.perf_counter() - start_time)

    total_time *= 1000 / SCALE_SAMPLES
    total_time = round(total_time, 2)
    print(
        f"(Task 2) Average time taken: {total_time} ms from {PERF_SAMPLES} samples")
# end_perf_test_task_2


def perf_test_task_3(coord: dict, cost: dict, dist: dict, g: dict) -> None:
    total_time = 0

    for _ in range(PERF_SAMPLES + 1):
        start_time = time.perf_counter()
        task3.astar('1', '50', ENERGY_BUDGET, coord, cost, dist, g, gamma=1)
        total_time += (time.perf_counter() - start_time)

    total_time *= 1000 / SCALE_SAMPLES
    total_time = round(total_time, 2)
    print(
        f"(Task 3) Average time taken: {total_time} ms from {PERF_SAMPLES} samples")
# end_perf_test_task_3


def scale_test_task_3(coord: dict, cost: dict, dist: dict, g: dict) -> None:
    for i in range(0, GAMMA_LIMIT*10 + 1, GAMMA_INCREMENT):
        # y = 0 to GAMMA_LIMIT, in increments of 0.2
        gamma = i / 10
        total_time = 0
        total_dist = 0

        for _ in range(SCALE_SAMPLES + 1):
            start_time = time.perf_counter()
            path = task3.astar('1', '50', ENERGY_BUDGET, coord,
                               cost, dist, g, gamma=gamma)

            total_time += (time.perf_counter() - start_time)
            total_dist += path.dist

        total_time *= 1000 / SCALE_SAMPLES
        total_time = round(total_time, 2)

        total_dist /= SCALE_SAMPLES
        total_dist = round(total_dist, 2)

        msg = f"For gamma: {gamma}, avg time taken: {total_time} ms, avg distance: {total_dist}"
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
