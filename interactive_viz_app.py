import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pdfplumber
from docx import Document
import io
from wordcloud import WordCloud

# ----------------------
# Custom CSS for dark/black theme with gradient background and sidebar styling
# ----------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #434343 100%);
        background-attachment: fixed;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.9);
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .css-1v3fvcr h2 {
        color: #FFD700;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stSelectbox, .stSlider, .stColorPicker {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid #555555;
        border-radius: 8px;
        color: #FFFFFF;
    }
    .stMarkdown {
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #333333;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------
# Word Cloud Functions
# ----------------------
def extract_text_from_word(iobytes):
    doc = Document(io.BytesIO(iobytes))
    paras = []
    for para in doc.paragraphs:
        paras.append(para.text)
    return ' '.join(paras)

def extract_text_from_pdf(iobytes):
    doc = pdfplumber.open(io.BytesIO(iobytes))
    pages = []
    for page in doc.pages:
        pages.append(page.extract_text())
    return ' '.join(pages)

def generate_wordcloud(uploaded):
    iobytes = uploaded.read()
    if uploaded.name.lower().endswith('pdf'):
        text = extract_text_from_pdf(iobytes)
    else:
        text = extract_text_from_word(iobytes)
    image = WordCloud(width=800, height=400, background_color='black', colormap='plasma').generate(text)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# ----------------------
# App Setup
# ----------------------
st.set_page_config(layout="wide")
st.title("🎨 Interactive Dashboard & Word Cloud App")
st.sidebar.header("Choose an Option")
app_mode = st.sidebar.selectbox("Select functionality:", ["Data Visualization", "Word Cloud Generator"])

# ----------------------
# Word Cloud Section
# ----------------------
if app_mode == "Word Cloud Generator":
    st.subheader("Generate Word Cloud from PDF or Word File")
    uploaded_wc = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
    if uploaded_wc is not None:
        generate_wordcloud(uploaded_wc)
    else:
        st.info("Please upload a PDF or Word file to generate the word cloud.")

# ----------------------
# Data Visualization Section
# ----------------------
elif app_mode == "Data Visualization":
    st.subheader("Upload or Generate Data for Visualization")
    st.sidebar.header("1️⃣ Provide Your Data")
    data_source = st.sidebar.radio("Choose data source:", ["Upload File", "Generate Random Data"])

    if data_source == "Upload File":
        file_types = ["csv", "xlsx", "txt"]
        file_format = st.sidebar.selectbox("Select File Type", file_types)
        uploaded_file = st.sidebar.file_uploader("Upload your data file", type=file_types)

        if uploaded_file is not None:
            try:
                if file_format == "csv":
                    df = pd.read_csv(uploaded_file)
                elif file_format == "xlsx":
                    df = pd.read_excel(uploaded_file)
                elif file_format == "txt":
                    try:
                        df = pd.read_csv(uploaded_file, sep="\t")
                    except:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, sep=",")
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

    st.sidebar.header("2️⃣ Select Columns")
    all_columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to include", all_columns, default=all_columns)

    if not selected_columns:
        st.error("Please select at least one column.")
        st.stop()

    df = df[selected_columns]
    st.write("### 📂 Filtered Data")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if not numeric_cols:
        st.error("No numeric columns available for visualization.")
        st.stop()

    st.sidebar.header("3️⃣ Visualization Settings")
    viz_type = st.sidebar.selectbox("Choose Visualization Type", ["1D", "2D", "3D"])

    st.sidebar.header("4️⃣ Aesthetics Settings")
    # Common colors
    bg_color = st.sidebar.color_picker("Background Color", "#222222")

    # Individual color pickers depending on visualization type
    if viz_type == "1D":
        marker_color = st.sidebar.color_picker("Marker/Bar Color", "#FF6347")
        edge_color = st.sidebar.color_picker("Edge Color", "#FFFFFF")
        line_color = st.sidebar.color_picker("Line Color", "#1E90FF")
        marker_size = st.sidebar.slider("Marker Size", 10, 200, 50)
        line_style = st.sidebar.selectbox("Line Style", ["-", "--", "-.", ":"])
        bins = st.sidebar.slider("Number of bins", 5, 50, 20)

        st.sidebar.subheader("1D Plot Options")
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Line Plot", "Bar Plot"])
        col = st.sidebar.selectbox("Select Column", numeric_cols)

        st.write(f"### 📈 {plot_type} of {col}")
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        if plot_type == "Histogram":
            ax.hist(df[col], bins=bins, color=marker_color, edgecolor=edge_color)
        elif plot_type == "Line Plot":
            ax.plot(df[col], marker="o", markersize=marker_size//10, linestyle=line_style, color=line_color)
        elif plot_type == "Bar Plot":
            ax.bar(df.index, df[col], color=marker_color, edgecolor=edge_color)

        ax.set_xlabel(col)
        ax.set_ylabel("Value")
        ax.set_title(f"{plot_type} of {col}", color="white")
        st.pyplot(fig)

    elif viz_type == "2D":
        marker_color = st.sidebar.color_picker("Marker Color", "#00CED1")
        edge_color = st.sidebar.color_picker("Edge Color", "#FFD700")
        line_color = st.sidebar.color_picker("Line Color", "#FF4500")
        marker_size = st.sidebar.slider("Marker Size", 10, 200, 50)
        line_style = st.sidebar.selectbox("Line Style", ["-", "--", "-.", ":"])

        st.sidebar.subheader("2D Plot Options")
        plot_type = st.sidebar.selectbox("Select Plot Type", ["Scatter Plot", "Box Plot", "Line Plot"])
        x_col = st.sidebar.selectbox("Select X-axis", numeric_cols)
        y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)

        st.write(f"### 📊 {plot_type} ({x_col} vs {y_col})")
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        if plot_type == "Scatter Plot":
            ax.scatter(df[x_col], df[y_col], c=marker_color, edgecolors=edge_color, alpha=0.8, s=marker_size)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
        elif plot_type == "Box Plot":
            df[[x_col, y_col]].plot(kind="box", ax=ax, color=dict(boxes=marker_color, whiskers=edge_color, medians=line_color, caps=edge_color))
        elif plot_type == "Line Plot":
            ax.plot(df[x_col], df[y_col], marker="o", markersize=marker_size//10, linestyle=line_style, color=line_color, markerfacecolor=marker_color)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)

        ax.set_title(f"{plot_type} of {x_col} & {y_col}", color="white")
        st.pyplot(fig)

    elif viz_type == "3D":
        marker_color = st.sidebar.color_picker("Point Color", "#FF69B4")
        edge_color = st.sidebar.color_picker("Edge Color", "#40E0D0")
        surface_color = st.sidebar.color_picker("Surface Color", "#32CD32")
        marker_size = st.sidebar.slider("Point Size", 10, 200, 50)

        st.sidebar.subheader("3D Plot Options")
        plot_type = st.sidebar.selectbox("Select Plot Type", ["3D Scatter Plot", "3D Surface Plot"])
        x_col = st.sidebar.selectbox("Select X-axis", numeric_cols)
        y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)
        z_col = st.sidebar.selectbox("Select Z-axis", numeric_cols)

        st.write(f"### 🧩 {plot_type}")
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        fig.patch.set_facecolor(bg_color)
        # ax.set_facecolor(bg_color) # 3D axes may not support set_facecolor in matplotlib

        if plot_type == "3D Scatter Plot":
            ax.scatter(df[x_col], df[y_col], df[z_col], c=marker_color, edgecolors=edge_color, alpha=0.8, s=marker_size)
            ax.set_xlabel(x_col, color="white")
            ax.set_ylabel(y_col, color="white")
            ax.set_zlabel(z_col, color="white")
        elif plot_type == "3D Surface Plot":
            X, Y = np.meshgrid(df[x_col], df[y_col])
            Z = np.sin(X) + np.cos(Y)
            ax.plot_surface(X, Y, Z, color=surface_color, alpha=0.7)
            ax.set_xlabel(x_col, color="white")
            ax.set_ylabel(y_col, color="white")
            ax.set_zlabel("Calculated", color="white")

        ax.set_title(plot_type, color="white")
        st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.markdown(" 🎉 Have fun exploring your data or generating word clouds! Customize and experiment freely! 🚀📊✨")

