import streamlit as st  # Importing the Streamlit library
import networkx as nx  # Importing NetworkX for graph manipulation
import matplotlib.pyplot as plt  # Importing Matplotlib for plotting
import graphviz  # Importing Graphviz for visualization
from networkx.drawing.nx_agraph import to_agraph  # Importing to_agraph for exporting to Graphviz format

# Function to output nodes and edges of a graph
def output_nodes_and_edges(graph: nx.Graph):
    st.write(graph.nodes)
    st.write(graph.edges)

# Function to count the number of nodes in a graph
def count_nodes(graph: nx.Graph):
    count = graph.number_of_nodes()
    st.info(f"Total number of nodes are {count}")

# Function to check if there is a path between two nodes in a graph
def check_path(graph: nx.Graph, ):
    node1_col, node2_col = st.columns(2)
    with node1_col:
        node1_select = st.selectbox("Select first node", options=graph.nodes, key="node1_select")
    with node2_col:
        node2_select = st.selectbox("Select second node", options=graph.nodes, key="node2_select")

    if node1_select and node2_select and nx.has_path(graph, node1_select, node2_select):
        st.success(f"There is a path between node {node1_select} and node {node2_select}.")
    else:
        st.error(f"There is no path between node {node1_select} and node {node2_select}.")

# Function to check if a graph is empty
def is_empty(graph: nx.Graph):
    is_graph_empty = nx.is_empty(graph)

    if is_graph_empty:
        st.info("The graph is empty.")
    else:
        st.info("The graph is not empty.")

# Function to check if a graph is directed
def is_directed(graph: nx.Graph):
    is_graph_directed = nx.is_directed(graph)
    if is_graph_directed:
        st.info("The graph is directed.")
    else:
        st.info("The graph is not directed")

# Function to display information about a specific node in a graph
def specific_node(graph: nx.Graph):
    node_select = st.selectbox("Select node", options=graph.nodes, key="node_select")
    node = graph.nodes[node_select]
    st.info(node)

# Function to display information about a specific edge in a graph
def specific_edge(graph: nx.Graph):
    node1_col, node2_col = st.columns(2)
    with node1_col:
        node1_select = st.selectbox("Select first node", options=graph.nodes, key="node1_select")
    with node2_col:
        node2_select = st.selectbox("Select second node", options=graph.nodes, key="node2_select")

    if node1_select == node2_select:
        st.warning("Please select two different nodes.")
    else:
        show_edge_button = st.button("Show edge details", use_container_width=True, type="primary")
        if show_edge_button:
            edge = graph.edges[node1_select, node2_select]
            if edge:
                st.info(edge)
            else:
                st.info(f"Edge {node1_select} to {node2_select} does not exist.")

# Function to calculate and display the density of a graph
def find_density(graph: nx.Graph):
    density = nx.density(graph)
    st.info(f"The density of graph is {density}")

# Function to calculate and display the shortest path between two nodes in a graph
def shortest_path(graph: nx.Graph):
    node1_col, node2_col = st.columns(2)

    # Get the list of nodes from the graph
    node_list = list(graph.nodes)

    with node1_col:
        node1_select = st.selectbox("Select first node", options=node_list, key="node1_select")

    # Remove the selected start node from the options for the target node selection
    target_node_options = [node for node in node_list if node != node1_select]

    with node2_col:
        node2_select = st.selectbox("Select second node", options=target_node_options, key="node2_select")

    try:
        shortest_path_for_graph = nx.shortest_path(graph, node1_select, node2_select)
        st.success(f"The shortest path between {node1_select} and {node2_select} is {shortest_path_for_graph}")
        subgraph = graph.subgraph(shortest_path_for_graph)

        graphviz_graph = graphviz.Digraph()
        for node in subgraph.nodes:
            graphviz_graph.node(str(node))

        for edge in subgraph.edges:
            graphviz_graph.edge(str(edge[0]), str(edge[1]))
        st.graphviz_chart(graphviz_graph)
    except nx.NetworkXNoPath:
        st.error(f"There is no path between {node1_select} and {node2_select}")


# Function to calculate and display the shortest paths from a selected start node to all other nodes in a graph
def show_shortest_paths(graph: nx.DiGraph):  # Rectified code of Prof. Luder
    try:
        graph_dict_tree = st.session_state["graph_dict"]
        node_list_tree = graph_dict_tree["nodes"]
        edge_list_tree = graph_dict_tree["edges"]
        node_list_tree_found = []
        edge_list_tree_found = []
        node_name_list_tree = [node["name"] for node in node_list_tree]

        start_node_select_tree = st.selectbox(
            "Select the start node of the shortest paths",
            options=node_name_list_tree
        )

        # Remove the selected start node from the options for target node selection
        target_node_options = [node for node in node_name_list_tree if node != start_node_select_tree]
        target_node_select_tree = st.selectbox(
            "Select the target node of the shortest paths",
            options=target_node_options
        )

        is_tree_button = st.button("Calculate trees", use_container_width=True, type="primary")

        if is_tree_button:
            tree_list = nx.shortest_path(graph, source=start_node_select_tree, target=target_node_select_tree,
                                         weight="dist")

            if not tree_list:
                st.write(f"There is no tree starting from {start_node_select_tree}.")
            else:
                for tree in tree_list:
                    st.write(f"The node {tree} is a member of the tree")
                    for node_element in node_list_tree:
                        if node_element["name"] == tree:
                            to_be_assigned_element = node_element
                            if to_be_assigned_element not in node_list_tree_found:
                                node_list_tree_found.append(node_element)

                for edge_element in edge_list_tree:
                    for source_node in node_list_tree_found:
                        for sink_node in node_list_tree_found:
                            if edge_element["source"] == source_node["name"] and edge_element["target"] == \
                                    sink_node["name"]:
                                edge_list_tree_found.append(edge_element)

                show_graph_without_weights(node_list_tree_found, edge_list_tree_found)
    except nx.NetworkXNoPath:
        st.error(f"There is no path between {start_node_select_tree} and {target_node_select_tree}")


# Function to display the graph without considering the weights of the edges
def show_graph_without_weights(nodes, edges):
    def set_color(node_type):
        color = "Grey"
        if node_type == "Person":
            color = "Blue"
        elif node_type == "Node":
            color = "Green"
        return color

    import graphviz
    graph = graphviz.Digraph()
    for node in nodes:
        node_name = node["name"]
        graph.node(node_name, color=set_color(node["type"]))
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        label = edge["type"]
        graph.edge(source, target, label)
    st.graphviz_chart(graph)

def minimum_spanning_tree(graph: nx.Graph):
    G = nx.Graph()
    edge_list=st.session_state["edge_list"]
    for edge in edge_list:
        G.add_edge(edge["source"], edge["target"], weight=edge["dist"])
    minimum_spanning_tree_graph=nx.minimum_spanning_tree(G)

    graphviz_graph = graphviz.Digraph()
    for node in minimum_spanning_tree_graph.nodes:
        graphviz_graph.node(str(node))

    for edge in minimum_spanning_tree_graph.edges:
        graphviz_graph.edge(str(edge[0]), str(edge[1]))
    st.graphviz_chart(graphviz_graph)

def spanning_tree(graph: nx.Graph):
    root_node = st.selectbox(
        "Select the start node of the shortest paths",
        options=graph.nodes
    )

    G = nx.Graph()
    edge_list=st.session_state["edge_list"]
    for edge in edge_list:
        G.add_edge(edge["source"], edge["target"], weight=edge["dist"])
    spanning_tree_graph=nx.dfs_tree(G, source=root_node)

    graphviz_graph = graphviz.Digraph()
    for node in spanning_tree_graph.nodes:
        graphviz_graph.node(str(node))

    for edge in spanning_tree_graph.edges:
        graphviz_graph.edge(str(edge[0]), str(edge[1]))
    st.graphviz_chart(graphviz_graph)
