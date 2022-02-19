from misc import ENERGY_BUDGET, load_json_files
import task1
import task2
import task3


def main():
    coord, cost, dist, g = load_json_files()

    run_task_1(dist, g)
    run_task_2(cost, dist, g)
    run_task_3(coord, cost, dist, g)
# end_main


def run_task_1(dist: dict, g: dict, printout: bool = True):
    path1 = task1.get_path('1', '50', dist, g)
    if printout:
        print("Task 1")
        print(f"Shortest path: {path1.path}")
        print(f"Shortest distance: {path1.dist}")
        print(f"Total energy cost: {path1.energy}\n")
# end_run_task_1


def run_task_2(cost: dict, dist: dict, g: dict, printout: bool = True):
    path2 = task2.get_path('1', '50', ENERGY_BUDGET, cost, dist, g)
    if printout:
        print("Task 2")
        print(f"Shortest path: {path2.path}")
        print(f"Shortest distance: {path2.dist}")
        print(f"Total energy cost: {path2.energy}\n")
# end_run_task_2


def run_task_3(coord: dict, cost: dict, dist: dict, g: dict, printout: bool = True):
    path3 = task3.get_path('1', '50', ENERGY_BUDGET, coord, cost, dist, g)
    if printout:
        print("Task 3")
        print(f"Shortest path: {path3.path}")
        print(f"Shortest distance: {path3.dist}")
        print(f"Total energy cost: {path3.energy}\n")
# end_run_task_2


if __name__ == "__main__":
    main()
