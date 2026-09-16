import pytest

from route_optimizer.graph import Graph
from route_optimizer.algorithms.dijkstra import dijkstra


def test_dijkstra_finds_shortest_distances():
    graph = Graph()

    graph.add_edge("A", "B", 10)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "D", 3)
    graph.add_edge("D", "B", 1)

    distances = dijkstra(graph, "A")

    assert distances["A"] == 0
    assert distances["B"] == 6
    assert distances["C"] == 2
    assert distances["D"] == 5


def test_dijkstra_rejects_negative_weights():
    graph = Graph()
    graph.add_edge("A", "B", -5)

    with pytest.raises(ValueError):
        dijkstra(graph, "A")