from collections import deque


def bfs(graph, start):
    visited = set()
    queue = deque()
    order = []

    visited.add(start)
    queue.append(start)

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbour, weight in graph.neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order