import heapq
from itertools import count


def astar(graph, start, destination, heuristic=None):
    nodes = graph.nodes()

    if start not in nodes:
        raise KeyError(f"Start node {start!r} does not exist.")

    if destination not in nodes:
        raise KeyError(f"Destination node {destination!r} does not exist.")

    if heuristic is None:
        heuristic = lambda node, goal: 0

    # Dijkstra and A* both require non-negative weights.
    for node in nodes:
        for neighbour, weight in graph.neighbours(node):
            if weight < 0:
                raise ValueError("A* does not support negative edge weights.")

    distances = {node: float("inf") for node in nodes}
    distances[start] = 0

    previous = {}
    counter = count()

    # Entries: (estimated total cost, unique ID, node)
    queue = [(heuristic(start, destination), next(counter), start)]

    while queue:
        estimated_cost, _, current = heapq.heappop(queue)

        if current == destination:
            path = []
            node = destination

            while node != start:
                path.append(node)
                node = previous[node]

            path.append(start)
            path.reverse()

            return path, distances[destination]

        for neighbour, weight in graph.neighbours(current):
            new_distance = distances[current] + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

                priority = new_distance + heuristic(neighbour, destination)

                heapq.heappush(
                    queue,
                    (priority, next(counter), neighbour)
                )

    return None, float("inf")