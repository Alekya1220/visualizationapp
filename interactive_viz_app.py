import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(layout="wide")
st.title("🎨 Streamlined Interactive Visualization Dashboard")
st.markdown("Upload or generate data, choose visualization types, and customize aesthetics in a unified interface!")

# ----------------------
# Data input section
# ----------------------
st.sidebar.header("1️⃣ Provide Your Data")

data_source = st.sidebar.radio("Choose data source:", ["Upload File", "Generate Random Data"])

if data_source == "Upload File":
    file_types = ["csv", "xlsx"]
    file_format = st.sidebar.selectbox("Select File Type", file_types)
    uploaded_file = st.sidebar.file_uploader("Upload your data file", type=file_types)

    if uploaded_file is not None:
        try:
            if file_format == "csv":
                df = pd.read_csv(uploaded_file)
            elif file_format == "xlsx":
                df = pd.read_excel(uploaded_file)
            st.success("File uploaded and loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()
    else:
        st.warning("Please upload a file to proceed.")
        st.stop()

elif data_source == "Generate Random Data":
    st.sidebar.subheader("Random Data Settings")
    n_samples = st.sidebar.slider("Number of samples", 50, 1000, 200)
    np.random.seed(42)
    df = pd.DataFrame({
        "X": np.random.randn(n_samples),
        "Y": np.random.randn(n_samples),
        "Z": np.random.randn(n_samples) * 10,
    })
    st.success("Random data generated!")

st.write("### 📋 Data Preview")
st.dataframe(df.head())

# ----------------------
# Select numeric columns
# ----------------------
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if not numeric_cols:
    st.error("No numeric columns available for visualization.")
    st.stop()

# ----------------------
# Visualization selection integrated
# ----------------------
st.sidebar.header("2️⃣ Visualization Type")

viz_options = [
    "1D → Histogram",
    "1D → Line Plot",
    "1D → Bar Plot",
    "2D → Scatter Plot",
    "2D → Box Plot",
    "2D → Line Plot",
    "3D → Scatter Plot",
    "3D → Surface Plot"
]
viz_type = st.sidebar.selectbox("Choose Visualization Type", viz_options)

# ----------------------
# Aesthetic settings
# ----------------------
st.sidebar.header("3️⃣ Aesthetics Settings")
color = st.sidebar.color_picker("Pick a color", "#FF6347")
marker_size = st.sidebar.slider("Marker Size", 10, 200, 50)
line_style = st.sidebar.selectbox("Line Style", ["-", "--", "-.", ":"])
bins = st.sidebar.slider("Number of bins", 5, 50, 20)

# ----------------------
# Visualization logic
# ----------------------

# 1D Plots
if viz_type.startswith("1D"):
    st.sidebar.subheader("Select Column")
    col = st.sidebar.selectbox("Select Column", numeric_cols)
    st.write(f"### 📈 {viz_type} of {col}")
    fig, ax = plt.subplots()

    if viz_type == "1D → Histogram":
        ax.hist(df[col], bins=bins, color=color, edgecolor="black")
    elif viz_type == "1D → Line Plot":
        ax.plot(df[col], marker="o", linestyle=line_style, color=color)
    elif viz_type == "1D → Bar Plot":
        ax.bar(df.index, df[col], color=color)

    ax.set_xlabel(col)
    ax.set_ylabel("Value")
    ax.set_title(f"{viz_type} of {col}")
    st.pyplot(fig)

# 2D Plots
elif viz_type.startswith("2D"):
    st.sidebar.subheader("Select Columns")
    x_col = st.sidebar.selectbox("Select X-axis", numeric_cols)
    y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)
    st.write(f"### 📊 {viz_type} ({x_col} vs {y_col})")
    fig, ax = plt.subplots()

    if viz_type == "2D → Scatter Plot":
        ax.scatter(df[x_col], df[y_col], c=color, alpha=0.6, s=marker_size)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
    elif viz_type == "2D → Box Plot":
        df[[x_col, y_col]].plot(kind="box", ax=ax)
    elif viz_type == "2D → Line Plot":
        ax.plot(df[x_col], df[y_col], marker="o", linestyle=line_style, color=color)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    ax.set_title(f"{viz_type} of {x_col} & {y_col}")
    st.pyplot(fig)

# 3D Plots
elif viz_type.startswith("3D"):
    st.sidebar.subheader("Select Columns")
    x_col = st.sidebar.selectbox("Select X-axis", numeric_cols)
    y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)
    z_col = st.sidebar.selectbox("Select Z-axis", numeric_cols)
    st.write(f"### 🧩 {viz_type}")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if viz_type == "3D → Scatter Plot":
        ax.scatter(df[x_col], df[y_col], df[z_col], c=color, alpha=0.6, s=marker_size)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
    elif viz_type == "3D → Surface Plot":
        X, Y = np.meshgrid(df[x_col], df[y_col])
        Z = np.sin(X) + np.cos(Y)
        ax.plot_surface(X, Y, Z, cmap="viridis")

    ax.set_title(viz_type)
    st.pyplot(fig)

# ----------------------
# Footer
# ----------------------
st.sidebar.markdown("---")
st.sidebar.write("App built with Streamlit ✅ Customize your visuals interactively!")
