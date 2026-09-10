class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, source, destination, weight=1):
        self.add_node(source)
        self.add_node(destination)

        self.adjacency_list[source].append((destination, weight))
        self.adjacency_list[destination].append((source, weight))

    def neighbours(self, node):
        if node not in self.adjacency_list:
            raise KeyError(f"Node {node!r} does not exist.")

        return self.adjacency_list[node]

    def nodes(self):
        return list(self.adjacency_list.keys())