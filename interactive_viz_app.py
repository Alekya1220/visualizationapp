import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(layout="wide")
st.title("🎨 Interactive Visualization Dashboard")
st.markdown("Upload your dataset and explore it with customizable visualizations!")

# ----------------------
# Data upload section
# ----------------------
st.sidebar.header("1️⃣ Upload Your Data")

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
    st.warning("Please upload a data file to proceed.")
    st.stop()

st.write("### 📋 Data Preview")
st.dataframe(df.head())

# ----------------------
# Select numeric columns dynamically
# ----------------------
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if not numeric_cols:
    st.error("No numeric columns available for visualization.")
    st.stop()

# ----------------------
# Visualization settings
# ----------------------
st.sidebar.header("2️⃣ Visualization Settings")
viz_type = st.sidebar.selectbox("Choose Visualization Type", ["1D", "2D", "3D"])

# ----------------------
# Color and style options
# ----------------------
st.sidebar.header("3️⃣ Aesthetics Settings")

color = st.sidebar.color_picker("Pick a color", "#FF6347")
marker_size = st.sidebar.slider("Marker Size", 10, 200, 50)
line_style = st.sidebar.selectbox("Line Style", ["-", "--", "-.", ":"])
bins = st.sidebar.slider("Number of bins", 5, 50, 20)

# ----------------------
# 1D Visualization
# ----------------------
if viz_type == "1D":
    st.sidebar.subheader("1D Plot Options")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Line Plot", "Bar Plot"])
    col = st.sidebar.selectbox("Select Column", numeric_cols)

    st.write(f"### 📈 {plot_type} of {col}")
    fig, ax = plt.subplots()

    if plot_type == "Histogram":
        ax.hist(df[col], bins=bins, color=color, edgecolor="black")
    elif plot_type == "Line Plot":
        ax.plot(df[col], marker="o", linestyle=line_style, color=color)
    elif plot_type == "Bar Plot":
        ax.bar(df.index, df[col], color=color)

    ax.set_xlabel(col)
    ax.set_ylabel("Value")
    ax.set_title(f"{plot_type} of {col}")
    st.pyplot(fig)

# ----------------------
# 2D Visualization
# ----------------------
elif viz_type == "2D":
    st.sidebar.subheader("2D Plot Options")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Scatter Plot", "Box Plot"])
    x_col = st.sidebar.selectbox("Select X-axis", numeric_cols)
    y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)

    st.write(f"### 📊 {plot_type} ({x_col} vs {y_col})")
    fig, ax = plt.subplots()

    if plot_type == "Scatter Plot":
        ax.scatter(df[x_col], df[y_col], c=color, alpha=0.6, s=marker_size)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
    elif plot_type == "Box Plot":
        df[[x_col, y_col]].plot(kind="box", ax=ax, color=color)

    ax.set_title(f"{plot_type} of {x_col} & {y_col}")
    st.pyplot(fig)

# ----------------------
# 3D Visualization
# ----------------------
elif viz_type == "3D":
    st.sidebar.subheader("3D Plot Options")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["3D Scatter Plot", "3D Surface Plot"])
    x_col = st.sidebar.selectbox("Select X-axis", numeric_cols)
    y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)
    z_col = st.sidebar.selectbox("Select Z-axis", numeric_cols)

    st.write(f"### 🧩 {plot_type}")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if plot_type == "3D Scatter Plot":
        ax.scatter(df[x_col], df[y_col], df[z_col], c=color, alpha=0.6, s=marker_size)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
    elif plot_type == "3D Surface Plot":
        X, Y = np.meshgrid(df[x_col], df[y_col])
        Z = np.sin(X) + np.cos(Y)
        ax.plot_surface(X, Y, Z, cmap="viridis")

    ax.set_title(plot_type)
    st.pyplot(fig)

# ----------------------
# Footer
# ----------------------
st.sidebar.markdown("---")
st.sidebar.write("App built with Streamlit ✅ Customize your visuals interactively!")
