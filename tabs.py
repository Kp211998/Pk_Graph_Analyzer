import streamlit as st  # Importing the Streamlit library
import uuid  # Importing UUID for generating unique identifiers
from model import metamodel_dict  # Importing model dictionary from a custom module
import json  # Importing JSON library for handling JSON data
import graphviz  # Importing Graphviz for visualization
from streamlit_agraph import agraph, Node, Edge, Config  # Importing agraph for graph visualization
import networkx as nx  # Importing NetworkX for graph analysis
from graph_functions import (output_nodes_and_edges, count_nodes, is_empty, find_density, is_directed, check_path,
                             specific_node, specific_edge, shortest_path,
                             show_shortest_paths, spanning_tree, minimum_spanning_tree)  # Importing custom graph functions
import time

# Function to upload graph from JSON
def upload_graph():
    uploaded_nodes = [],
    uploaded_edges = []
    uploaded_graph = st.file_uploader("Upload an existing graph", type="json")  # Uploading JSON file

    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        uploaded_nodes = uploaded_graph_dict["nodes"]
        uploaded_edges = uploaded_graph_dict["edges"]
    else:
        st.info("Please upload graph if available")

    update_graph_button = st.button("Update Graph", use_container_width=True, type="primary",
                                    disabled=uploaded_graph is None)  # Button to update graph

    if update_graph_button:
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["edge_list"] = uploaded_edges
        update_graph_dict()

def update_graph_dict():
    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"],
    }
    st.session_state["graph_dict"] = graph_dict

# Function to create a node
def create_node():
    name_node = st.text_input("Type the name of node : ", placeholder="Name of Node")
    type_node = st.selectbox("Specify the type of node", ["Node", "Person"])
    age_node = st.number_input("Type your age: ", value=0, min_value=0)
    save_node_button = st.button("Save Details", use_container_width=True, type="primary")

    if save_node_button:
        save_node(name_node, age_node, type_node)
        st.toast('Node Details Saved Successfully')
        st.info(f'Hi, My name is {name_node} and I am {age_node} years old')

# Function to save node details
def save_node(name, age, type_of_node):
    node_dict = {
        "name": name,
        "age": age,
        "id": str(uuid.uuid4()),
        "type": type_of_node
    }
    st.session_state["node_list"].append(node_dict)

# Function to update a node
def update_node():
    node_list = st.session_state["node_list"]
    node_names = [node["name"] for node in node_list]

    try:
        # Select the node to update
        node_to_update = st.selectbox("Select node to update", options=node_names)

        # Find the index of the selected node in the list
        selected_index = node_names.index(node_to_update)
        selected_node = node_list[selected_index]

        # Display current node properties
        st.write(f"Current properties of node '{node_to_update}':")
        st.write(selected_node)

        # Allow users to update node properties
        new_name = st.text_input("Enter new name for the node", value=selected_node["name"])
        new_age = st.number_input("Enter new age for the node", value=selected_node["age"])
        new_type = st.selectbox("Select new type for the node", options=["Node", "Person"])
        update_node_button = st.button("Update Node", key="update_node_button",use_container_width=True, type="primary")

        if update_node_button:
            # Update node properties
            node_list[selected_index]["name"] = new_name
            node_list[selected_index]["age"] = new_age
            node_list[selected_index]["type"] = new_type

            # Update session state with the modified node list
            st.session_state["node_list"] = node_list

            st.success(f"Node '{node_to_update}' has been updated.")

    except ValueError:
        st.error("There are no nodes added yet. Please create nodes or import a graph")

# Function to delete a node
def delete_node():
    node_list = st.session_state["node_list"]
    node_names = [node["name"] for node in node_list]

    node_to_delete = st.selectbox("Select node to delete", options=node_names)
    delete_node_button = st.button("Delete Node", key="delete_node_button", use_container_width=True, type="primary")

    if delete_node_button:
        # Remove the node from the node list
        st.session_state["node_list"] = [node for node in node_list if node["name"] != node_to_delete]

        # Remove edges connected to the deleted node from the edge list
        st.session_state["edge_list"] = [edge for edge in st.session_state["edge_list"]
                                         if edge["source"] != node_to_delete and edge["target"] != node_to_delete]

        st.session_state["deleted_node"] = node_to_delete  # Store the deleted node name

        st.success(f"Node '{node_to_delete}' has been deleted.")
        time.sleep(1)
        st.experimental_rerun()
# Function to create a relation
def create_relation():
    node1_col, relation_col, node2_col = st.columns(3)
    node_list = st.session_state["node_list"]
    node_name_list = [node["name"] for node in node_list]

    with node1_col:
        node1_select = st.selectbox("Select first node", options=node_name_list, key="node1_select")

    with relation_col:
        relation_list = metamodel_dict["edges"]
        relation_name = st.selectbox("Specify the relation", options=relation_list)

    with node2_col:
        node2_select = st.selectbox("Select second node", options=node_name_list, key="node2_select")

    if node1_select == node2_select:
        st.warning("Please select two different nodes.")
    else:
        existing_edges = st.session_state["edge_list"]
        edge_exists = any(
            edge["source"] == node1_select and edge["target"] == node2_select and edge["type"] == relation_name
            for edge in existing_edges
        )
        if edge_exists:
            st.error(f"A relation of type '{relation_name}' already exists between '{node1_select}' and '{node2_select}'.")
        else:
            store_edge_button = st.button("Save Relationship", use_container_width=True, type="primary")
            if store_edge_button:
                save_edge(node1_select, relation_name, node2_select)
                st.write(f"{node1_select} is {relation_name} {node2_select}")

# Function to save edge details
def save_edge(node1, relation, node2):
    edge_dict = {
        "source": node1,
        "target": node2,
        "type": relation,
        "id": str(uuid.uuid4())
    }
    st.session_state["edge_list"].append(edge_dict)

# Function to update an edge
def update_edge():
    edge_list = st.session_state["edge_list"]

    try:
        # Create a list of edge descriptions for user selection
        edge_descriptions = [f"{edge['source']} -> {edge['target']} ({edge['type']})" for edge in edge_list]

        # Select the edge to update
        selected_edge_description = st.selectbox("Select edge to update", options=edge_descriptions)

        # Find the index of the selected edge in the list
        selected_index = edge_descriptions.index(selected_edge_description)
        selected_edge = edge_list[selected_index]

        # Display current edge properties
        st.write(f"Current properties of edge '{selected_edge_description}':")
        st.write(selected_edge)

        # Extract source and target nodes from the selected edge
        source_node = selected_edge["source"]
        target_node = selected_edge["target"]

        # Allow users to update edge properties
        new_source = st.selectbox("Select new source node for the edge",
                                  options=[node["name"] for node in st.session_state["node_list"]],
                                  index=[node["name"] for node in st.session_state["node_list"]].index(source_node))
        new_target = st.selectbox("Select new target node for the edge",
                                  options=[node["name"] for node in st.session_state["node_list"]],
                                  index=[node["name"] for node in st.session_state["node_list"]].index(target_node))

        # Check if the source and target nodes are the same
        if new_source == new_target:
            st.error("Source and target nodes cannot be the same.")
        else:
            new_type = st.selectbox("Select new type for the edge", options=metamodel_dict["edges"],
                                    index=metamodel_dict["edges"].index(selected_edge["type"]))
            update_edge_button = st.button("Update Edge", key="update_edge_button", type="primary",
                                           use_container_width=True)

            if update_edge_button:
                # Update edge properties
                edge_list[selected_index]["source"] = new_source
                edge_list[selected_index]["target"] = new_target
                edge_list[selected_index]["type"] = new_type

                # Update session state with the modified edge list
                st.session_state["edge_list"] = edge_list

                st.success(f"Edge '{selected_edge_description}' has been updated.")

    except ValueError:
        st.error("There are no relations added yet. Please create relations between nodes or import a graph")

# Function to delete an edge
def delete_edge():
    edge_list = st.session_state["edge_list"]
    edge_sources = [edge["source"] for edge in edge_list]
    edge_targets = [edge["target"] for edge in edge_list]
    edge_ids = [edge["id"] for edge in edge_list]

    # Construct options for the selection boxes
    edge_options = [f"{edge_sources[i]} to {edge_targets[i]}" for i in range(len(edge_list))]

    # Select edge to delete
    edge_to_delete = st.selectbox("Select edge to delete",key="edge_to_delete", options=edge_options)
    delete_edge_button=st.button("Delete Edge", key="delete_edge_button", type="primary",use_container_width=True)

    if delete_edge_button:
        # Find the index of the selected edge in the options list
        selected_index = edge_options.index(edge_to_delete)

        # Remove the selected edge from the edge list using its index
        del edge_list[selected_index]

        # Update the session state with the modified edge list
        st.session_state["edge_list"] = edge_list

        st.success(f"Edge '{edge_to_delete}' has been deleted.")
        time.sleep(1)
        st.experimental_rerun()

# Function to display stored graph details
def store_graph():
    with st.expander("Show Individual Lists"):
        st.json(st.session_state["node_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)

    with st.expander("Show Graph JSON", expanded=False):
        st.json(st.session_state["graph_dict"])

# Function to visualize graph using Graphviz and Agraph
def visualize_graph():
    update_graph_dict()

    def set_color(node_type):
        color = 'grey'
        if node_type == 'Person':
            color = 'green'
        elif node_type == 'Node':
            color = 'red'
        elif node_type == 'Resource':
            color = 'blue'
        return color

    with st.expander("Show Graph", expanded=False):
        graph = graphviz.Digraph()
        graph_dict = st.session_state["graph_dict"]
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]

        for node in node_list:
            node_name = node["name"]
            graph.node(node_name, color=set_color(node["type"]))

        for edge in edge_list:
            source = edge["source"]
            target = edge["target"]
            label = edge["type"]
            graph.edge(source, target, label)

        st.graphviz_chart(graph)

    with st.expander("Agraph visualization", expanded=False):
        nodes = []
        edges = []

        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]

        for node in node_list:
            nodes.append(Node(id=node['name'], label=node["name"]))

        for edge in edge_list:
            edges.append(Edge(source=edge['source'], target=edge['target'], label=edge["type"]))

        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        heirarchical=False,
                        nodeHighlightBehavior=True,
                        highlightColor="#F7A7A6",
                        collapsible=False,
                        )

        agraph(nodes=nodes,
               edges=edges,
               config=config)

# Function to analyze graph
def analyze_graph():
    g = nx.DiGraph()
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    node_tuple_list = []
    edge_tuple_list = []

    for node in node_list:
        node_tuple = (node["name"], node)
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["source"], edge["target"], edge)
        edge_tuple_list.append(edge_tuple)

    g.add_nodes_from(node_tuple_list)
    g.add_edges_from(edge_tuple_list)

    select_function = st.selectbox(label="Select function",
                                   options=["Output nodes and edges", 'Count nodes', "Show specific node",
                                            "Show specific edge", "Check Path", "Check if Graph is Empty",
                                            "Density of Graph", "Is Graph Directed", "Find shortest Path",
                                            "Show shortest Path(Soln of Prof.Luder)","Spanning Tree", "Minimum Spanning Tree"])

    if select_function == "Output nodes and edges":
        output_nodes_and_edges(graph=g)
    elif select_function == "Count nodes":
        count_nodes(graph=g)
    elif select_function == "Check Path":
        check_path(graph=g, )
    elif select_function == "Check if Graph is Empty":
        is_empty(graph=g)
    elif select_function == "Density of Graph":
        find_density(graph=g)
    elif select_function == "Is Graph Directed":
        is_directed(graph=g)
    elif select_function == "Show specific node":
        specific_node(graph=g)
    elif select_function == "Show specific edge":
        specific_edge(graph=g)
    elif select_function == "Find shortest Path":
        shortest_path(g)
    elif select_function == "Show shortest Path(Soln of Prof.Luder)":
        show_shortest_paths(g)
    elif select_function == "Spanning Tree":
        spanning_tree(g)
    elif select_function == "Minimum Spanning Tree":
        minimum_spanning_tree(g)

# Function to export graph to JSON
def export_graph():
    visualize_graph()
    graph_string = json.dumps(st.session_state["graph_dict"])

    st.download_button("Export Graph to JSON",
                       file_name="graph.json",
                       mime="application/json",
                       data=graph_string,
                       use_container_width=True,
                       type="primary"
                       )
