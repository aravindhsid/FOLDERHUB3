import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="Interactive Data Visualizer", layout="wide")

# Title
st.title("📊 Interactive Data Visualizer")
st.write("Upload your dataset and create **interactive visualizations** with Plotly!")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load data
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        st.stop()

    st.success("✅ File uploaded successfully!")

    # Data preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Sidebar options
    st.sidebar.header("⚙️ Visualization Settings")

    all_columns = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Plot type selection
    plot_type = st.sidebar.radio(
        "Choose a visualization type:",
        ("Bar Chart", "Scatter Plot", "Line Chart", "Pie Chart")
    )

    st.subheader("📈 Visualization")

    if plot_type == "Bar Chart":
        x_axis = st.selectbox("Select X-axis", all_columns, key="bar_x")
        y_axis = st.selectbox("Select Y-axis", numeric_cols, key="bar_y")
        fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, title="Bar Chart")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Scatter Plot":
        x_axis = st.selectbox("Select X-axis", numeric_cols, key="scatter_x")
        y_axis = st.selectbox("Select Y-axis", numeric_cols, key="scatter_y")
        color_col = st.selectbox("Select color column (optional)", [None] + all_columns, key="scatter_color")
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, title="Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Line Chart":
        x_axis = st.selectbox("Select X-axis", all_columns, key="line_x")
        y_axis = st.selectbox("Select Y-axis", numeric_cols, key="line_y")
        fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_type == "Pie Chart":
        cat_col = st.selectbox("Select categorical column", all_columns, key="pie_cat")
        num_col = st.selectbox("Select numeric column", numeric_cols, key="pie_num")
        fig = px.pie(df, names=cat_col, values=num_col, title="Pie Chart")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 Upload a dataset to get started")
