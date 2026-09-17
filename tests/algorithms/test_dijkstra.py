import pytest

from route_optimizer.graph import Graph
from route_optimizer.algorithms.dijkstra import dijkstra, reconstruct_path


def test_dijkstra_finds_shortest_distances():
    graph = Graph()

    graph.add_edge("A", "B", 10)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "D", 3)
    graph.add_edge("D", "B", 1)

    distances, previous = dijkstra(graph, "A")

    assert distances["A"] == 0
    assert distances["B"] == 6
    assert distances["C"] == 2
    assert distances["D"] == 5

    assert previous["C"] == "A"
    assert previous["D"] == "C"
    assert previous["B"] == "D"


def test_dijkstra_rejects_negative_weights():
    graph = Graph()
    graph.add_edge("A", "B", -5)

    with pytest.raises(ValueError):
        dijkstra(graph, "A")


def test_reconstruct_path():
    previous = {
        "C": "A",
        "D": "C",
        "B": "D"
    }

    path = reconstruct_path(previous, "A", "B")

    assert path == ["A", "C", "D", "B"]


def test_reconstruct_path_returns_none_when_unreachable():
    previous = {
        "B": "A"
    }

    path = reconstruct_path(previous, "A", "C")

    assert path is None