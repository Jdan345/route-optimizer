import random
import statistics
import sys
import time
from pathlib import Path

# Allow running this script from the project root
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from route_optimizer.graph import Graph
from route_optimizer.algorithms.dijkstra import shortest_path
from route_optimizer.algorithms.astar import astar


def build_random_graph(number_of_nodes, seed=42):
    """Create a connected graph with positive edge weights."""
    rng = random.Random(seed)
    graph = Graph()

    for node in range(number_of_nodes):
        graph.add_node(node)

    # Connect every node to the next, ensuring connectivity.
    for node in range(number_of_nodes - 1):
        graph.add_edge(node, node + 1, rng.randint(1, 20))

    # Add additional random edges.
    for _ in range(number_of_nodes * 3):
        source, destination = rng.sample(
            range(number_of_nodes), 2
        )
        graph.add_edge(
            source,
            destination,
            rng.randint(1, 20),
        )

    return graph


def measure_runtime(function, repetitions=20):
    """Return median execution time in milliseconds."""
    timings = []

    for _ in range(repetitions):
        start_time = time.perf_counter()
        function()
        elapsed = time.perf_counter() - start_time
        timings.append(elapsed * 1000)

    return statistics.median(timings)


def run_benchmark():
    print("\nRoute Optimizer — Algorithm Benchmark")
    print("-" * 65)
    print(
        f"{'Nodes':<10}"
        f"{'Dijkstra (ms)':<20}"
        f"{'A* (ms)':<20}"
        f"{'Costs match'}"
    )
    print("-" * 65)

    for size in [50, 100, 250, 500]:
        graph = build_random_graph(size)

        start_node = 0
        destination_node = size - 1

        dijkstra_result = shortest_path(
            graph, start_node, destination_node
        )

        # A* with a zero heuristic provides a fair correctness
        # baseline without inventing a heuristic for random graphs.
        astar_result = astar(
            graph, start_node, destination_node
        )

        costs_match = (
            dijkstra_result[1] == astar_result[1]
        )

        dijkstra_time = measure_runtime(
            lambda: shortest_path(
                graph, start_node, destination_node
            )
        )

        astar_time = measure_runtime(
            lambda: astar(
                graph, start_node, destination_node
            )
        )

        print(
            f"{size:<10}"
            f"{dijkstra_time:<20.4f}"
            f"{astar_time:<20.4f}"
            f"{str(costs_match)}"
        )


if __name__ == "__main__":
    run_benchmark()
