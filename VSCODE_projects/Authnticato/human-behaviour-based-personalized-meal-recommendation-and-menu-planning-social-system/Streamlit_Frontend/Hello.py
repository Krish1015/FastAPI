import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Human Behavior Based Personalized Meal "
         "Recommendation and Menu Planning Social System")

st.sidebar.success("Select a recommendation app.")

st.markdown(
    """
    Using content-based approach with Scikit-Learn, FastAPI and Streamlit.
 
    """
)
