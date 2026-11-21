
import math

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from route_optimizer.graph import Graph
from route_optimizer.algorithms.dijkstra import shortest_path
from route_optimizer.algorithms.astar import astar


st.set_page_config(
    page_title="Route Optimizer",
    page_icon="🗺️",
    layout="wide",
)


def build_network():
    graph = Graph()

    roads = [
        ("Southampton", "Winchester", 14),
        ("Southampton", "Portsmouth", 30),
        ("Southampton", "Salisbury", 25),
        ("Winchester", "Basingstoke", 30),
        ("Winchester", "Salisbury", 35),
        ("Portsmouth", "Chichester", 25),
        ("Chichester", "Guildford", 50),
        ("Basingstoke", "Reading", 25),
        ("Basingstoke", "Guildford", 40),
        ("Reading", "Oxford", 40),
        ("Reading", "London", 65),
        ("Guildford", "London", 50),
        ("Oxford", "London", 90),
        ("Salisbury", "Oxford", 95),
    ]

    for source, destination, distance in roads:
        graph.add_edge(source, destination, distance)

    return graph, roads


graph, roads = build_network()

# Illustrative coordinates, not real GPS positions.
positions = {
    "Southampton": (1, 1),
    "Winchester": (2, 2),
    "Portsmouth": (3, 0),
    "Salisbury": (0, 2),
    "Basingstoke": (3, 3),
    "Chichester": (5, 0),
    "Guildford": (5, 2),
    "Reading": (4, 4),
    "Oxford": (3, 6),
    "London": (7, 4),
}


def geographical_heuristic(node, destination):
    x1, y1 = positions[node]
    x2, y2 = positions[destination]

    straight_line_distance = math.hypot(x2 - x1, y2 - y1)

    # Conservative estimate for this illustrative network.
    return straight_line_distance


def draw_network(roads, path=None):
    network = nx.Graph()

    for source, destination, distance in roads:
        network.add_edge(source, destination, weight=distance)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Draw all nodes
    nx.draw_networkx_nodes(
        network,
        positions,
        node_color="#DCEBFA",
        node_size=1500,
        ax=ax,
    )

    # Draw all roads
    nx.draw_networkx_edges(
        network,
        positions,
        edge_color="#A0A0A0",
        width=2,
        ax=ax,
    )

    # Draw city names
    nx.draw_networkx_labels(
        network,
        positions,
        font_size=9,
        font_weight="bold",
        ax=ax,
    )

    # Display edge weights
    edge_labels = nx.get_edge_attributes(network, "weight")

    nx.draw_networkx_edge_labels(
        network,
        positions,
        edge_labels=edge_labels,
        font_size=8,
        ax=ax,
    )

    # Highlight the selected route
    if path and len(path) > 1:
        route_edges = list(zip(path[:-1], path[1:]))

        nx.draw_networkx_edges(
            network,
            positions,
            edgelist=route_edges,
            edge_color="#087EFA",
            width=5,
            ax=ax,
        )

        nx.draw_networkx_nodes(
            network,
            positions,
            nodelist=path,
            node_color="#6AB6FF",
            node_size=1500,
            ax=ax,
        )

        nx.draw_networkx_labels(
            network,
            positions,
            font_size=9,
            font_weight="bold",
            ax=ax,
        )

    ax.set_axis_off()
    fig.tight_layout()

    return fig


# -------------------------
# Streamlit user interface
# -------------------------

st.title("🗺️ Route Optimizer")

st.write(
    "Compare Dijkstra's algorithm and A* on a weighted road network."
)

st.caption(
    "Demonstration network with illustrative edge weights "
    "and node positions, not verified real-world distances."
)

cities = sorted(graph.nodes())

col1, col2, col3 = st.columns(3)

with col1:
    start = st.selectbox(
        "Starting city",
        cities,
        index=cities.index("Southampton"),
    )

with col2:
    destination = st.selectbox(
        "Destination",
        cities,
        index=cities.index("London"),
    )

with col3:
    algorithm = st.selectbox(
        "Algorithm",
        ["Dijkstra", "A*"],
    )


# -------------------------
# Calculate shortest route
# -------------------------

if algorithm == "Dijkstra":
    path, distance = shortest_path(graph, start, destination)
else:
    path, distance = astar(
        graph,
        start,
        destination,
        heuristic=geographical_heuristic,
    )


# -------------------------
# Display results
# -------------------------

st.divider()

if path is None:
    st.warning("No route exists between these cities.")
else:
    st.metric("Total route cost", f"{distance:g}")
    st.success(" → ".join(path))

figure = draw_network(roads, path)
st.pyplot(figure)
plt.close(figure)

st.caption(
    "Dijkstra explores routes by known cost. "
    "A* uses a straight-line heuristic based on illustrative "
    "node coordinates to guide its search."
)
