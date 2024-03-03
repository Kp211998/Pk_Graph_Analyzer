import streamlit as st  # Importing the Streamlit library
from streamlit_option_menu import option_menu  # Importing a custom module for creating an option menu
from tabs import (upload_graph, create_node, delete_node, create_relation, store_graph,
                  visualize_graph, analyze_graph, export_graph, delete_edge, update_node, update_edge)  # Importing functions from a custom module for various tabs

# Setting the page configuration for Streamlit app
st.set_page_config(layout="wide", initial_sidebar_state="auto")

# Checking if certain session state variables exist, if not, initializing them
if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []

    # Setting the title of the Streamlit app
    st.title("Graph Analyzer by Prathamesh")

    # List of tabs for the Streamlit app
    tab_list = [
        "Import Graph",
        "Create Node",
        "Update Node",
        "Delete Node",
        "Create Relations",
        "Update Relations",
        "Delete Relations",
        "Store the Graph",
        "Visualize the Graph",
        "Analyze the Graph",
        "Export the Graph"
    ]

    # Creating a sidebar with an option menu for selecting the main menu
    with st.sidebar:
        selected = option_menu("Main Menu", tab_list,
                               menu_icon="cast",
                               default_index=0,
                               )

    # Handling the selected tab and calling the corresponding function
    if selected == "Import Graph":
        upload_graph()  # Function call to upload graph
    if selected == "Create Node":
        create_node()  # Function call to create node
    if selected == "Update Node":
        update_node()  # Function call to update node
    if selected == "Delete Node":
        delete_node()  # Function call to delete node
    if selected == "Create Relations":
        create_relation()  # Function call to create relations
    if selected == "Update Relations":
        update_edge()  # Function call to update relations
    if selected == "Delete Relations":
        delete_edge()  # Function call to delete relations
    if selected == "Store the Graph":
        store_graph()  # Function call to store the graph
    if selected == "Visualize the Graph":
        visualize_graph()  # Function call to visualize the graph
    if selected == "Analyze the Graph":
        analyze_graph()  # Function call to analyze the graph
    if selected == "Export the Graph":
        export_graph()  # Function call to export the graph
