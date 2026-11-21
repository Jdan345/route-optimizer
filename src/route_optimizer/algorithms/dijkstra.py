import heapq


def dijkstra(graph, start):
    if start not in graph.nodes():
        raise KeyError(f"Start node {start!r} does not exist.")

    distances = {}
    previous = {}

    for node in graph.nodes():
        distances[node] = float("inf")

    distances[start] = 0

    queue = []
    heapq.heappush(queue, (0, start))

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # Skip outdated priority queue entries
        if current_distance > distances[current_node]:
            continue

        for neighbour, weight in graph.neighbours(current_node):
            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm does not support negative edge weights."
                )

            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_node

                heapq.heappush(queue, (new_distance, neighbour))

    return distances, previous


def reconstruct_path(previous, start, destination):
    path = []
    current = destination

    while current != start:
        if current not in previous:
            return None

        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return path


def shortest_path(graph, start, destination):
    if destination not in graph.nodes():
        raise KeyError(f"Destination node {destination!r} does not exist.")

    distances, previous = dijkstra(graph, start)

    path = reconstruct_path(previous, start, destination)
    distance = distances[destination]

    return path, distance