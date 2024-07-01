import streamlit as st
import pandas as pd
import math
from graphviz import Digraph
import streamlit.components.v1 as components
import traceback
from c45_functions import build_tree, TreeNode

def main():
    st.title('Decision Tree Visualization')
    st.sidebar.title('File Upload')

    # File upload and DataFrame creation
    uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xls", "xlsx"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write('### Dataset:')
            st.write(df)

            st.header('Tree Structure:')
            examples = df.to_dict(orient='records')
            # tree = id3(examples, target_attribute, attributes)
            tree = build_tree(df)

            # Create a Digraph object
            dot = Digraph(comment='Tree')

            # Add nodes and edges to the Digraph
            tree.add_to_dot(dot)

            # Render the tree in Streamlit
            st.graphviz_chart(dot.source)
            #with st.expander("Decision Tree"):
            #    tree.add_to_flow(st)
        except Exception as e:
            st.error(f"Error: {e}")
            st.error(traceback.format_exc())

if __name__ == '__main__':
    main()
