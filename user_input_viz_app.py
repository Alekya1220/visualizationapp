import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.title("📊 User Input Visualization App")

# -------------------------------
# User input
# -------------------------------
st.sidebar.header("Input Options")

# Number of samples
n_samples = st.sidebar.slider("Number of Samples", min_value=10, max_value=500, value=100)

# Generate data
np.random.seed(42)
df = pd.DataFrame({
    "X": np.random.randn(n_samples),
    "Y": np.random.randn(n_samples),
    "Z": np.random.randn(n_samples) * 10,
})

st.write("### Data Preview")
st.dataframe(df.head())

# -------------------------------
# Visualization type
# -------------------------------
viz_type = st.sidebar.selectbox("Choose Visualization Type", ["1D", "2D", "3D"])

# -------------------------------
# 1D Visualizations
# -------------------------------
if viz_type == "1D":
    plot_type = st.sidebar.selectbox("Choose 1D Plot", ["Histogram", "Line", "Bar"])
    col = st.sidebar.selectbox("Select Column", df.columns)

    fig, ax = plt.subplots()
    if plot_type == "Histogram":
        bins = st.sidebar.slider("Number of bins", 5, 50, 20)
        ax.hist(df[col], bins=bins, color="skyblue", edgecolor="black")
        ax.set_title(f"Histogram of {col}")
    elif plot_type == "Line":
        ax.plot(df[col], marker="o")
        ax.set_title(f"Line Plot of {col}")
    elif plot_type == "Bar":
        ax.bar(df.index, df[col], color="orange")
        ax.set_title(f"Bar Plot of {col}")
    st.pyplot(fig)

# -------------------------------
# 2D Visualizations
# -------------------------------
elif viz_type == "2D":
    plot_type = st.sidebar.selectbox("Choose 2D Plot", ["Scatter", "Box"])
    x_col = st.sidebar.selectbox("X-axis", df.columns)
    y_col = st.sidebar.selectbox("Y-axis", df.columns)

    fig, ax = plt.subplots()
    if plot_type == "Scatter":
        size = st.sidebar.slider("Marker Size", 10, 200, 50)
        ax.scatter(df[x_col], df[y_col], c="red", alpha=0.6, s=size)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"Scatter Plot: {x_col} vs {y_col}")
    elif plot_type == "Box":
        df[[x_col, y_col]].plot(kind="box", ax=ax)
        ax.set_title(f"Box Plot of {x_col} & {y_col}")
    st.pyplot(fig)

# -------------------------------
# 3D Visualizations
# -------------------------------
elif viz_type == "3D":
    plot_type = st.sidebar.selectbox("Choose 3D Plot", ["3D Scatter", "3D Surface"])
    x_col = st.sidebar.selectbox("X-axis", df.columns)
    y_col = st.sidebar.selectbox("Y-axis", df.columns)
    z_col = st.sidebar.selectbox("Z-axis", df.columns)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if plot_type == "3D Scatter":
        ax.scatter(df[x_col], df[y_col], df[z_col], c="blue", alpha=0.6)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
        ax.set_title("3D Scatter Plot")

    elif plot_type == "3D Surface":
        # For surface plot, we create a grid
        X, Y = np.meshgrid(df[x_col], df[y_col])
        Z = np.sin(X) + np.cos(Y)
        ax.plot_surface(X, Y, Z, cmap="viridis")
        ax.set_title("3D Surface Plot")

    st.pyplot(fig)
