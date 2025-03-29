import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

# Custom styling
st.set_page_config(
    page_title="Mild Steel Degradation Analysis Dashboard",
    page_icon=None,
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #692475;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #A47DAB;
    }
    .uploadedFile {
        border: 2px solid #82AB7D;
        border-radius: 5px;
        padding: 1rem;
    }
    .css-1d391kg {
        background-color: #6A6B4E;
    }
    h1 {
        color: #692475 !important;
    }
    h2 {
        color: #82AB7D !important;
    }
    h3 {
        color: #6A6B4E !important;
    }
    .sidebar .sidebar-content {
        background-color: #f8f5fa;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #692475;'>About</h2>", unsafe_allow_html=True)
    
    # Project Information
    st.markdown("""
        <div style='background-color: #A47DAB22; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <h3 style='color: #82AB7D; margin-top: 0;'>Project Overview</h3>
            <p>This tool analyzes microscopic images of mild steel surfaces to assess degradation over time.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Analysis Methods
    st.markdown("""
        <div style='background-color: #82AB7D22; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <h3 style='color: #692475; margin-top: 0;'>Analysis Methods</h3>
            <ul>
                <li>CLAHE Enhancement</li>
                <li>Adaptive Thresholding</li>
                <li>Morphological Operations</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Explanation
    st.markdown("""
        <div style='background-color: #69247522; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <h3 style='color: #82AB7D; margin-top: 0;'>Metrics Guide</h3>
            <p><b>Degradation %:</b> Percentage of degraded surface area</p>
            <p><b>Mean Intensity:</b> Average brightness of the surface</p>
            <p><b>Std Intensity:</b> Variation in surface texture</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tips
    st.markdown("""
        <div style='background-color: #6A6B4E22; padding: 1rem; border-radius: 5px;'>
            <h3 style='color: #692475; margin-top: 0;'>Tips</h3>
            <ul>
                <li>Use high-resolution images</li>
                <li>Ensure consistent lighting</li>
                <li>Maintain same magnification</li>
                <li>Clean surfaces before imaging</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Version info at bottom
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>Version 1.0.0</small>
        </div>
    """, unsafe_allow_html=True)

def process_image(image, clip_limit=3.0, grid_size=8, block_size=31, c_value=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
    enhanced_gray = clahe.apply(gray)
    thresh = cv2.adaptiveThreshold(enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, block_size, c_value)
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    return thresh, enhanced_gray

def calculate_metrics(processed_image, original_gray):
    degradation_percentage = np.count_nonzero(processed_image) / (processed_image.shape[0] * processed_image.shape[1]) * 100
    mean_intensity = np.mean(original_gray)
    std_intensity = np.std(original_gray)
    return {
        "Degradation %": round(degradation_percentage, 2),
        "Mean Intensity": round(mean_intensity, 2),
        "Std Intensity": round(std_intensity, 2)
    }

def save_report(degradation_data):
    csv = BytesIO()
    pd.DataFrame(degradation_data).to_csv(csv, index=False)
    csv.seek(0)
    return csv

def plot_degradation(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    df_pivot = df.pivot(index="Image", columns="Stage", values="Degradation %")
    
    colors = ['#A47DAB', '#692475', '#82AB7D', '#6A6B4E']
    for idx, img in enumerate(df_pivot.index):
        plt.plot(df_pivot.columns, df_pivot.loc[img], marker='o', 
                linestyle='-', label=img, color=colors[idx % len(colors)])
    
    plt.xlabel("Time Stage")
    plt.ylabel("Degradation Percentage (%)")
    plt.title("Degradation Progression Over Time")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.grid(True, alpha=0.3)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    st.pyplot(fig)

st.title("Mild Steel Degradation Analysis Dashboard")
st.markdown("""
    <div style='background-color: #A47DAB22; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;'>
        Upload microscopic images of different stages to analyze degradation over time.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color: #692475;'>Initial Stages</h3>", unsafe_allow_html=True)
    np_file = st.file_uploader("Upload Newly Painted (NP) Image", type=["jpg", "png", "jpeg"])
    y1_file = st.file_uploader("Upload 1 Year (1Y) Image", type=["jpg", "png", "jpeg"])
    y1b_file = st.file_uploader("Upload 1 Year Brushed (1YB) Image", type=["jpg", "png", "jpeg"])

with col2:
    st.markdown("<h3 style='color: #692475;'>Later Stages</h3>", unsafe_allow_html=True)
    y5_file = st.file_uploader("Upload 5 Years (5Y) Image", type=["jpg", "png", "jpeg"])
    y5b_file = st.file_uploader("Upload 5 Years Brushed (5YB) Image", type=["jpg", "png", "jpeg"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Analyze Degradation"):
    uploaded_files = [np_file, y1_file, y1b_file, y5_file, y5b_file]
    labels = ["Newly Painted", "1 Year", "1 Year Brushed", "5 Years", "5 Years Brushed"]
    degradation_data = []

    st.markdown("<h2>Analysis Results</h2>", unsafe_allow_html=True)
    result_cols = st.columns(len(uploaded_files))
    
    for i, file in enumerate(uploaded_files):
        if file:
            image = Image.open(file)
            image = np.array(image)
            processed_image, enhanced_gray = process_image(
                image, 
                clip_limit=3.0,
                grid_size=8,
                block_size=31,
                c_value=5
            )
            
            metrics = calculate_metrics(processed_image, enhanced_gray)
            degradation_data.append({
                "Image": file.name,
                "Stage": labels[i],
                **metrics
            })
            
            with result_cols[i]:
                st.markdown(f"<h4 style='color: #82AB7D;'>{labels[i]}</h4>", unsafe_allow_html=True)
                st.image(file, caption=f"Original", use_container_width=True)
                st.image(processed_image, caption=f"Processed", use_container_width=True)
                
                st.markdown(
                    f"""<div style='background-color: #69247522; padding: 1rem; border-radius: 5px; text-align: center;'>
                        <h3 style='margin: 0; color: #692475;'>{metrics['Degradation %']}%</h3>
                        <p style='margin: 0;'>Degradation</p>
                    </div>""",
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    f"""<div style='background-color: #82AB7D22; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                        <p><b>Mean Intensity:</b> {metrics['Mean Intensity']}</p>
                        <p><b>Std Intensity:</b> {metrics['Std Intensity']}</p>
                    </div>""",
                    unsafe_allow_html=True
                )
    
    if degradation_data:
        st.markdown("<h2>Degradation Report</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(degradation_data)
        
        display_cols = ['Image', 'Stage', 'Degradation %', 'Mean Intensity', 'Std Intensity']
        st.dataframe(
            df[display_cols].style.background_gradient(cmap='RdYlGn_r', subset=['Degradation %'])
        )
        
        csv_file = save_report(degradation_data)
        st.download_button(
            "Download Report",
            csv_file,
            "degradation_report.csv",
            "text/csv",
            key='download-csv'
        )
        
        st.markdown("<h2>Degradation Over Time</h2>", unsafe_allow_html=True)
        plot_degradation(df)
