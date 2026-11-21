import pytest

from route_optimizer.graph import Graph
from route_optimizer.algorithms.astar import astar


def test_astar_finds_shortest_path():
    graph = Graph()

    graph.add_edge("A", "B", 10)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "D", 3)
    graph.add_edge("D", "B", 1)

    path, distance = astar(graph, "A", "B")

    assert path == ["A", "C", "D", "B"]
    assert distance == 6


def test_astar_with_heuristic():
    graph = Graph()

    graph.add_edge("A", "B", 10)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "D", 3)
    graph.add_edge("D", "B", 1)

    estimates = {
        "A": 6,
        "B": 0,
        "C": 4,
        "D": 1,
    }

    def heuristic(node, destination):
        return estimates[node]

    path, distance = astar(graph, "A", "B", heuristic)

    assert path == ["A", "C", "D", "B"]
    assert distance == 6


def test_astar_unreachable():
    graph = Graph()

    graph.add_edge("A", "B", 5)
    graph.add_node("C")

    path, distance = astar(graph, "A", "C")

    assert path is None
    assert distance == float("inf")


def test_astar_same_start_and_destination():
    graph = Graph()
    graph.add_node("A")

    path, distance = astar(graph, "A", "A")

    assert path == ["A"]
    assert distance == 0


def test_astar_rejects_negative_weights():
    graph = Graph()
    graph.add_edge("A", "B", -5)

    with pytest.raises(ValueError):
        astar(graph, "A", "B")


def test_astar_rejects_missing_start():
    graph = Graph()
    graph.add_edge("A", "B")

    with pytest.raises(KeyError):
        astar(graph, "Missing", "B")


def test_astar_rejects_missing_destination():
    graph = Graph()
    graph.add_edge("A", "B")

    with pytest.raises(KeyError):
        astar(graph, "A", "Missing")