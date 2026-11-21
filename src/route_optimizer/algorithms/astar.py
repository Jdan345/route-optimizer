
import heapq
from itertools import count


def astar(graph, start, destination, heuristic=None):
    """
    Find a minimum-cost path using A* search.

    The heuristic must be admissible (never overestimate
    the remaining shortest-path cost) for optimal results.

    Returns:
        (path, cost), or (None, infinity) if unreachable.
    """

    nodes = graph.nodes()

    if start not in nodes:
        raise KeyError(f"Start node {start!r} does not exist.")

    if destination not in nodes:
        raise KeyError(
            f"Destination node {destination!r} does not exist."
        )

    if heuristic is None:
        heuristic = lambda node, goal: 0

    # A* requires non-negative edge weights.
    for node in nodes:
        for neighbour, weight in graph.neighbours(node):
            if weight < 0:
                raise ValueError(
                    "A* does not support negative edge weights."
                )

    distances = {
        node: float("inf") for node in nodes
    }
    distances[start] = 0

    previous = {}
    counter = count()

    # Queue entries: (estimated total, known cost, tie-breaker, node)
    queue = [
        (
            heuristic(start, destination),
            0,
            next(counter),
            start,
        )
    ]

    while queue:
        estimated_total, current_cost, _, current = heapq.heappop(
            queue
        )

        # Skip entries superseded by a cheaper route.
        if current_cost > distances[current]:
            continue

        if current == destination:
            path = []
            node = destination

            while node != start:
                path.append(node)
                node = previous[node]

            path.append(start)
            path.reverse()

            return path, current_cost

        for neighbour, weight in graph.neighbours(current):
            new_cost = current_cost + weight

            if new_cost < distances[neighbour]:
                distances[neighbour] = new_cost
                previous[neighbour] = current

                priority = (
                    new_cost + heuristic(neighbour, destination)
                )

                heapq.heappush(
                    queue,
                    (
                        priority,
                        new_cost,
                        next(counter),
                        neighbour,
                    ),
                )

    return None, float("inf")