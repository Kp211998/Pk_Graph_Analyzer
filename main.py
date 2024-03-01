import streamlit as st
from streamlit_option_menu import option_menu
from tabs import upload_graph, create_node, create_relation, store_graph, visualize_graph, analyze_graph, export_graph

# Press the green button in the gutter to run the script.
st.set_page_config(layout="wide", initial_sidebar_state="auto")

if __name__ == '__main__':
    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []
    st.title("Title given by PK")

    tab_list = [
        "Import Graph",
        "Create Node",
        "Create Relations",
        "Store the Graph",
        "Visualize the Graph",
        "Analyze the Graph",
        "Export the Graph"
    ]
    # import_graph_tab, create_node_tab, create_relation_tab, store_graph_tab, visualize_graph_tab, 
    # anaylze_graph_tab, export_graph_tab = st.tabs( tab_list )

    with st.sidebar:
        selected = option_menu("Main Menu", tab_list,
                               menu_icon="cast",
                               default_index=0,
                               )

    # with import_graph_tab:
    if selected == "Import Graph":
        upload_graph()

    # with create_relation_tab:
    if selected == "Create Node":
        create_node()

    # with create_relation_tab:
    if selected == "Create Relations":
        create_relation()

    # with store_graph_tab:
    if selected == "Store the Graph":
        store_graph()

    # with visualize_graph_tab:
    if selected == "Visualize the Graph":
        visualize_graph()

    # with anaylze_graph_tab:
    if selected == "Analyze the Graph":
        analyze_graph()

    # with export_graph_tab:
    if selected == "Export the Graph":
        export_graph()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
