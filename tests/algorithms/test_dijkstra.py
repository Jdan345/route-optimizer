import pytest

from route_optimizer.graph import Graph
from route_optimizer.algorithms.dijkstra import (
    dijkstra,
    reconstruct_path,
    shortest_path,
)


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
        "B": "D",
    }

    path = reconstruct_path(previous, "A", "B")

    assert path == ["A", "C", "D", "B"]


def test_reconstruct_path_returns_none_when_unreachable():
    previous = {"B": "A"}

    path = reconstruct_path(previous, "A", "C")

    assert path is None


def test_shortest_path():
    graph = Graph()

    graph.add_edge("A", "B", 10)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "D", 3)
    graph.add_edge("D", "B", 1)

    path, distance = shortest_path(graph, "A", "B")

    assert path == ["A", "C", "D", "B"]
    assert distance == 6


def test_shortest_path_unreachable():
    graph = Graph()

    graph.add_edge("A", "B", 5)
    graph.add_node("C")

    path, distance = shortest_path(graph, "A", "C")

    assert path is None
    assert distance == float("inf")


def test_dijkstra_rejects_missing_start():
    graph = Graph()
    graph.add_edge("A", "B")

    with pytest.raises(KeyError):
        dijkstra(graph, "Missing")


def test_shortest_path_rejects_missing_destination():
    graph = Graph()
    graph.add_edge("A", "B")

    with pytest.raises(KeyError):
        shortest_path(graph, "A", "Missing")