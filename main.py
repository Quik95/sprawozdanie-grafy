import csv
import gc
import os
import random
from timeit import Timer
from typing import List, Iterator, Tuple, Any, Dict

from macierz import AdjacencyMatrix


def topological_sort_no_sorting(data: Iterator[Tuple[str, int]]) -> Dict[int, List[int]]:
    time_values = {}
    i = 1
    for value_type, value in data:
        if value not in time_values:
            time_values[value] = [i, None]
        elif value_type == "out":
            time_values[value][1] = i
        i += 1
    return time_values


def topological_sort(data: Iterator[Tuple[str, int]]) -> List[int]:
    time_values = topological_sort_no_sorting(data)
    res = [(key, value[1]) for key, value in time_values.items()]
    return [key for key, value in reversed(sorted(res, key=lambda k: k[1]))]


def generate_random_graph(size: int, density: float) -> AdjacencyMatrix:
    matrix = AdjacencyMatrix()
    matrix.list = [[0 for _ in range(0, size)] for _ in range(0, size)]

    n = int(size * (size - 1) * density)

    for _ in range(n):
        i = 0
        j = 0
        while True:
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            if matrix.list[i][j] == 0 and i != j:
                break

        matrix.list[i][j] = 1
    # with open("/tmp/a", "w") as f:
    #     for row in matrix.list:
    #         f.write(",".join([str(i) for i in row]) + "\n")

    return matrix


def benchmark_function(name: str, f: Any) -> float:
    number_of_runs = 10 if "lista łuków" not in name else 1
    gc.collect()
    time_taken = Timer(f).timeit(number=number_of_runs) / number_of_runs
    print(f"{name}: {time_taken}s")
    return time_taken


def number_of_return_nodes(data: Dict[int, List[int]], matrix: AdjacencyMatrix) -> int:
    keys = list(data.keys())
    n = 0
    for i in range(0, len(keys)):
        for j in range(i + 1, len(keys)):
            v = keys[i]
            u = keys[j]
            if matrix.get(v, u) == 1 and data[v][0] < data[u][0] < data[u][1] < data[v][1]:
                n += 1
    return n


def save_measurement(name: str, measurements: List[float]):
    with open("wyniki.csv", "a+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, *measurements])


if __name__ == '__main__':
    try:
        os.remove("wyniki.csv")
    except FileNotFoundError:
        pass

    steps = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

    with open("wyniki.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(["name", *steps])

    sort_top_02 = []
    sort_top_04 = []

    n_powrotne_02 = []
    n_powrotne_04 = []

    time_mac_02 = []
    time_list_02 = []
    time_edge_02 = []

    time_mac_04 = []
    time_list_04 = []
    time_edge_04 = []

    for step in steps:
        print(f"{step=}")
        graph_density_02 = generate_random_graph(step, 0.2)
        graph_density_04 = generate_random_graph(step, 0.4)

        graph_density_02_list = graph_density_02.to_adjacency_list()
        graph_density_04_list = graph_density_04.to_adjacency_list()

        graph_density_02_edge = graph_density_02.to_list_of_edges()
        graph_density_04_edge = graph_density_04.to_list_of_edges()

        sort_top_02.append(benchmark_function('Sortowanie Topologiczne d=0.2',
                                              lambda: topological_sort_no_sorting(
                                                  graph_density_02_list.depth_first_search())))
        sort_top_04.append(benchmark_function('Sortowanie Topologiczne d=0.4',
                                              lambda: topological_sort_no_sorting(
                                                  graph_density_04_list.depth_first_search())))

        time_values = topological_sort_no_sorting(graph_density_02_list.depth_first_search())
        n_powrotne_02.append(graph_density_02.number_of_return_nodes(time_values))
        time_mac_02.append(benchmark_function("Zliczanie łuków powrotnych d=0.2 (macierz)",
                                              lambda: graph_density_02.number_of_return_nodes(time_values)))
        time_list_02.append(benchmark_function("Zliczanie łuków powrotnych d=0.2 (lista następników)",
                                               lambda: graph_density_02_list.number_of_return_nodes(time_values)))
        time_edge_02.append(benchmark_function("Zliczanie łuków powrotnych d=0.2 (lista łuków)",
                                               lambda: graph_density_02_edge.number_of_return_nodes(time_values)))

        time_values = topological_sort_no_sorting(graph_density_04_list.depth_first_search())
        n_powrotne_04.append(graph_density_04.number_of_return_nodes(time_values))
        time_mac_04.append(benchmark_function("Zliczanie łuków powrotnych d=0.4 (macierz)",
                                              lambda: graph_density_04.number_of_return_nodes(time_values)))
        time_list_04.append(benchmark_function("Zliczanie łuków powrotnych d=0.4 (lista następników)",
                                               lambda: graph_density_04_list.number_of_return_nodes(time_values)))
        time_edge_04.append(benchmark_function("Zliczanie łuków powrotnych d=0.4 (lista łuków)",
                                               lambda: graph_density_04_edge.number_of_return_nodes(time_values)))

    save_measurement("Sortowanie topologiczne d=0.2", sort_top_02)
    save_measurement("Sortowanie topologiczne d=0.4", sort_top_04)

    save_measurement("Liczba łuków powrotnych d=0.2", n_powrotne_02)
    save_measurement("Liczba łuków powrotnych d=0.4", n_powrotne_04)

    save_measurement("Czas macierz d=0.2", time_mac_02)
    save_measurement("Czas macierz d=0.4", time_mac_04)

    save_measurement("Czas lista d=0.2", time_list_02)
    save_measurement("Czas lista d=0.4", time_list_04)

    save_measurement("Czas lista łuków d=0.2", time_edge_02)
    save_measurement("Czas lista łuków d=0.4", time_edge_04)
