import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ------------------------
# App title
# ------------------------
st.set_page_config(layout="wide")
st.title("📊 Interactive Visualization Dashboard")
st.markdown("Use this app to explore your data with 1D, 2D, and 3D visualizations!")

# ------------------------
# Data input
# ------------------------
st.sidebar.header("1️⃣ Select Data Source")

data_source = st.sidebar.radio("Choose how to provide data:", ("Upload CSV file", "Generate Random Data"))

if data_source == "Upload CSV file":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
    else:
        st.warning("Please upload a CSV file to proceed.")
        st.stop()
else:
    st.sidebar.subheader("Random Data Options")
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

# ------------------------
# Visualization selection
# ------------------------
st.sidebar.header("2️⃣ Choose Visualization Type")
viz_type = st.sidebar.selectbox("Select Visualization Type", ["1D", "2D", "3D"])

# ------------------------
# 1D Visualization
# ------------------------
if viz_type == "1D":
    st.sidebar.subheader("1D Plot Settings")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Line Plot", "Bar Plot"])
    col = st.sidebar.selectbox("Select Column", df.columns)

    st.write(f"### 📈 {plot_type} of {col}")
    fig, ax = plt.subplots()
    
    if plot_type == "Histogram":
        bins = st.sidebar.slider("Number of bins", 5, 50, 20)
        ax.hist(df[col], bins=bins, color="skyblue", edgecolor="black")
    elif plot_type == "Line Plot":
        ax.plot(df[col], marker="o", linestyle="-")
    elif plot_type == "Bar Plot":
        ax.bar(df.index, df[col], color="orange")
    
    ax.set_xlabel(col)
    ax.set_ylabel("Value")
    ax.set_title(f"{plot_type} of {col}")
    st.pyplot(fig)

# ------------------------
# 2D Visualization
# ------------------------
elif viz_type == "2D":
    st.sidebar.subheader("2D Plot Settings")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Scatter Plot", "Box Plot"])
    x_col = st.sidebar.selectbox("X-axis", df.columns)
    y_col = st.sidebar.selectbox("Y-axis", df.columns)

    st.write(f"### 📊 {plot_type} ({x_col} vs {y_col})")
    fig, ax = plt.subplots()

    if plot_type == "Scatter Plot":
        size = st.sidebar.slider("Marker Size", 10, 200, 50)
        ax.scatter(df[x_col], df[y_col], c="red", alpha=0.6, s=size)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
    elif plot_type == "Box Plot":
        df[[x_col, y_col]].plot(kind="box", ax=ax)
    
    ax.set_title(f"{plot_type} of {x_col} & {y_col}")
    st.pyplot(fig)

# ------------------------
# 3D Visualization
# ------------------------
elif viz_type == "3D":
    st.sidebar.subheader("3D Plot Settings")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["3D Scatter Plot", "3D Surface Plot"])
    x_col = st.sidebar.selectbox("X-axis", df.columns)
    y_col = st.sidebar.selectbox("Y-axis", df.columns)
    z_col = st.sidebar.selectbox("Z-axis", df.columns)

    st.write(f"### 🧩 {plot_type}")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    if plot_type == "3D Scatter Plot":
        ax.scatter(df[x_col], df[y_col], df[z_col], c="blue", alpha=0.6)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
    elif plot_type == "3D Surface Plot":
        X, Y = np.meshgrid(df[x_col], df[y_col])
        Z = np.sin(X) + np.cos(Y)
        ax.plot_surface(X, Y, Z, cmap="viridis")
    
    ax.set_title(plot_type)
    st.pyplot(fig)

# ------------------------
# Footer
# ------------------------
st.sidebar.markdown("---")
st.sidebar.write("Interactive app built with Streamlit ✅")
