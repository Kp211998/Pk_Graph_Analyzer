import streamlit as st
import uuid
from model import metamodel_dict
import json
from streamlit_modal import Modal
import graphviz
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
from graph_functions import (output_nodes_and_edges, count_nodes, is_empty, find_density, is_directed, check_path,
                             specific_node, specific_edge, shortest_path)


def upload_graph():
    uploaded_nodes = [],
    uploaded_edges = []
    uploaded_graph = st.file_uploader("Upload an existing graph", type="json")

    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        # st.write(uploaded_graph_dict)
        uploaded_nodes = uploaded_graph_dict["nodes"]
        uploaded_edges = uploaded_graph_dict["edges"]

    else:
        st.info("Please upload graph if available")

    update_graph_button = st.button("Update Graph", use_container_width=True, type="primary",
                                    disabled=uploaded_graph is None)
    if update_graph_button:
        st.session_state["node_list"] = uploaded_nodes
        st.session_state["edge_list"] = uploaded_edges
        graph_dict = {
            "nodes": st.session_state["node_list"],
            "edges": st.session_state["edge_list"],
        }

        st.session_state["graph_dict"] = graph_dict



def create_node():
    modal = Modal(
        title="Thank You",
        key="vote-modal",
        padding=20,  # default value
        max_width=400,
    )
    name_node = st.text_input("Type the name of node : ")
    type_node = st.selectbox("Specify the type of node", ["Node", "Person"])
    age_node = st.number_input("Type your age: ", value=0)
    st.info(f'Hi, My name is {name_node} and I am {age_node} years old')
    save_node_button = st.button("Save Details", use_container_width=True, type="primary")
    if save_node_button:
        save_node(name_node, age_node, type_node)
        st.toast('Node Details Saved Successfully', icon='😍')
        modal.open()

    # if modal.is_open():
    #     with modal.container():
    #         st.text('Thank you for your vote to BJP')
    #         st.image('nm.jpeg', caption='', width=350)


def save_node(name, age, type_of_node):
    node_dict = {
        "name": name,
        "age": age,
        "id": str(uuid.uuid4()),
        "type": type_of_node
    }
    # st.write(node_dict)
    st.session_state["node_list"].append(node_dict)
    st.write(st.session_state["node_list"])


def create_relation():
    # Model logic
    node1_col, relation_col, node2_col = st.columns(3)
    node_list = st.session_state["node_list"]
    node_name_list = []
    for node in node_list:
        node_name_list.append(node["name"])
    # UI Rendering
    with node1_col:
        node1_select = st.selectbox("Select first node", options=node_name_list, key="node1_select")

    with relation_col:
        # Logic
        relation_list = metamodel_dict["edges"]

        # UI Rendering
        relation_name = st.selectbox("Specify the relation", options=relation_list)

    with node2_col:
        node2_select = st.selectbox("Select second node", options=node_name_list, key="node2_select")

    if node1_select == node2_select:
        st.warning("Please select two different node")
    store_edge_button = st.button("Save Relationship", use_container_width=True, type="primary",
                                  disabled=node1_select == node2_select)

    if store_edge_button:
        save_edge(node1_select, relation_name, node2_select)
    st.write(f"{node1_select} is {relation_name}  {node2_select}")
    # st.write(st.session_state["edge_list"])


# st.write(st.session_state["node_list"])

def save_edge(node1, relation, node2):
    edge_dict = {
        "source": node1,
        "target": node2,
        "type": relation,
        "id": str(uuid.uuid4())
    }
    st.session_state["edge_list"].append(edge_dict)


def store_graph():
    with st.expander("Show Individual Lists"):
        st.json(st.session_state["node_list"], expanded=False)
        st.json(st.session_state["edge_list"], expanded=False)

    with st.expander("Show Graph JSON", expanded=False):
        st.json(st.session_state["graph_dict"])


def visualize_graph():
    def set_color(node_type):
        color='grey'
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
            graph.node(node_name,color=set_color(node["type"]))

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

        # for edge in edge_list:
        #     for node in node_list:
        #         if edge["source"]==node["name"]:
        #             source=node["id"]
        #         elif edge["target"]==node["name"]:
        #             target=node["id"]
        #     edges.append(Edge(source=source, target=target, label=edge["type"]))

        for edge in edge_list:
            edges.append(Edge(source=edge['source'], target=edge['target'], label=edge["type"]))

        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        heirarchical=False,
                        nodeHighlightBehavior=True,
                        highlightColor="#F7A7A6",  # or "blue"
                        collapsible=False,
                        # coming soon (set for all): node_size=1000, node_color="blue"
                        )

        agraph(nodes=nodes,
               edges=edges,
               config=config)


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
    # st.write(g.nodes)
    # st.write(g.edges)

    select_function = st.selectbox(label="Select function",
                                   options=["Output nodes and edges", 'Count nodes', "Show specific node",
                                            "Show specific edge",
                                            "Check Path", "Check if Graph is Empty", "Density of Graph",
                                            "Is Graph Directed", "Find shortest Path"])
    if select_function == "Output nodes and edges":
        output_nodes_and_edges(graph=g)
    elif select_function == "Count nodes":
        count_nodes(graph=g)
    elif select_function == "Check Path":
        node1_col, node2_col = st.columns(2)
        with node1_col:
            node1_select = st.selectbox("Select first node", options=g.nodes, key="node1_select")
        with node2_col:
            node2_select = st.selectbox("Select second node", options=g.nodes, key="node2_select")
        if node1_select and node2_select:
            check_path(node1_select, node2_select, graph=g, )
    elif select_function == "Check if Graph is Empty":
        is_empty(graph=g)
    elif select_function == "Density of Graph":
        find_density(graph=g)
    elif select_function == "Is Graph Directed":
        is_directed(graph=g)
    elif select_function == "Show specific node":
        node_select = st.selectbox("Select node", options=g.nodes, key="node_select")
        specific_node(node_select, graph=g)
    elif select_function == "Show specific edge":
        node1_col, node2_col = st.columns(2)
        with node1_col:
            node1_select = st.selectbox("Select first node", options=g.nodes, key="node1_select")
        with node2_col:
            node2_select = st.selectbox("Select second node", options=g.nodes, key="node2_select")

        specific_edge_for_graph = specific_edge(node1_select, node2_select, graph=g, )
        if node1_select and node2_select and node1_select != node2_select and specific_edge_for_graph:
            st.write(specific_edge_for_graph)

    elif select_function == "Find shortest Path":
        shortest_path(g)



def export_graph():
    graph_string = json.dumps(st.session_state["graph_dict"])

    st.download_button("Export Graph to JSON",
                       file_name="graph.json",
                       mime="application/json",
                       data=graph_string,
                       use_container_width=True,
                       type="primary"
                       )


