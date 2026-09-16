import pytest

from route_optimizer.graph import Graph
from route_optimizer.algorithms.bfs import bfs


def test_add_node():
    graph = Graph()

    graph.add_node("Southampton")

    assert "Southampton" in graph.nodes()


def test_add_edge():
    graph = Graph()

    graph.add_edge("Southampton", "Winchester", 14)

    assert ("Winchester", 14) in graph.neighbours("Southampton")
    assert ("Southampton", 14) in graph.neighbours("Winchester")


def test_neighbours_raises_error_for_missing_node():
    graph = Graph()

    with pytest.raises(KeyError):
        graph.neighbours("London")


def test_add_duplicate_node():
    graph = Graph()

    graph.add_node("Southampton")
    graph.add_node("Southampton")

    assert graph.nodes() == ["Southampton"]


