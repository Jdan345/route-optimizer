import pytest

from route_optimizer.graph import Graph
from route_optimizer.algorithms.bfs import bfs


def test_bfs_traversal():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")

    result = bfs(graph, "A")

    assert result == ["A", "B", "C", "D", "E"]


def test_bfs_handles_cycles():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("D", "A")

    result = bfs(graph, "A")

    assert result == ["A", "B", "D", "C"]


def test_bfs_raises_error_for_missing_start_node():
    graph = Graph()
    graph.add_edge("A", "B")

    with pytest.raises(KeyError):
        bfs(graph, "London")