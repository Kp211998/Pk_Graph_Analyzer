import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from networkx.drawing.nx_agraph import to_agraph

def output_nodes_and_edges(graph: nx.Graph):
    st.write(graph.nodes)
    st.write(graph.edges)


def count_nodes(graph: nx.Graph):
    count = graph.number_of_nodes()
    st.info(f"Total number of nodes are {count}")


def check_path(node1, node2, graph: nx.Graph, ):
    if nx.has_path(graph, node1, node2):
        st.success(f"There is a path between node {node1} and node {node2}.")
    else:
        st.error(f"There is no path between node {node1} and node {node2}.")


def is_empty(graph: nx.Graph):
    is_graph_empty = nx.is_empty(graph)

    if is_graph_empty:
        st.info("The graph is empty.")
    else:
        st.info("The graph is not empty.")


def is_directed(graph: nx.Graph):
    is_graph_directed = nx.is_directed(graph)
    if is_graph_directed:
        st.info("The graph is directed.")
    else:
        st.info("The graph is not directed")


def specific_node(input_node, graph: nx.Graph):
    node = graph.nodes[input_node]
    st.info(node)


def specific_edge(node1, node2, graph: nx.Graph):
    edge = graph.edges[node1, node2]
    if edge:
        st.info(edge)
    else:
        st.info(f"Edge {node1} to {node2}  does not exist.")


def find_density(graph: nx.Graph):
    density = nx.density(graph)
    st.info(f"The density of graph is {density}")


def shortest_path(graph: nx.Graph):
    node1_col, node2_col = st.columns(2)
    with node1_col:
        node1_select = st.selectbox("Select first node", options=graph.nodes, key="node1_select")
    with node2_col:
        node2_select = st.selectbox("Select second node", options=graph.nodes, key="node2_select")

    try:
         shortest_path_for_graph = nx.shortest_path(graph,node1_select, node2_select)
         st.success(f"The shortest path between {node1_select} and {node2_select} is {shortest_path_for_graph}")
         subgraph=graph.subgraph(shortest_path_for_graph)

         graphviz_graph=graphviz.Digraph()
         for node in subgraph.nodes:
            graphviz_graph.node(str(node))

        # Add edges to the Graphviz object
         for edge in subgraph.edges:
            graphviz_graph.edge(str(edge[0]), str(edge[1]))
         st.graphviz_chart(graphviz_graph)
    except nx.NetworkXNoPath:
        st.error(f"There is no path between {node1_select} and {node2_select}")


# def shortest_path(graph:nx.DiGraph):
#     graph_dict_tree = st.session_state["graph_dict"]
#     node_list_tree = graph_dict_tree["nodes"]
#     edge_list_tree = graph_dict_tree["edges"]
#     node_list_tree_found = []
#     edge_list_tree_found = []
#     node_name_list_tree = []
#     for node in node_list_tree:
#         node_name_list_tree.append(node["name"])
#     start_node_select_tree = st.selectbox(
#             "Select the start node of the shortest paths",
#             options=node_name_list_tree
#         )
#     is_tree_button = st.button("Calculate trees", use_container_width=True, type="primary")
#     if is_tree_button:
#         tree_list = nx.shortest_path(graph, source=start_node_select_tree, weight="dist")
#         # st.write(tree_list)
#         if not tree_list:
#             st.write(f"There is no tree starting starting from {start_node_select_tree}.")
#         else:
#             for tree in tree_list:
#                 st.write(f" The node {tree} is member of the tree")
#                 for tree_element in tree:
#                     for node_element in node_list_tree:
#                         if node_element["name"] == tree_element:
#                             to_be_assigned_element = node_element
#                             if to_be_assigned_element not in node_list_tree_found:
#                                 node_list_tree_found.append(node_element)
#             # print(node_list_tree_found)
#             for edge_element in edge_list_tree:
#                 for source_node in node_list_tree_found:
#                     for sink_node in node_list_tree_found:
#                         if edge_element["source"] == source_node["name"] and edge_element["target"] == sink_node["name"]:
#                             edge_list_tree_found.append(edge_element)
#             # print(edge_element)
#             # show_graph_withoutweights(node_list_tree_found, edge_list_tree_found)


