import streamlit as st

st.set_page_config(page_title="Documentation - Mild Steel Degradation Analysis Dashboard", layout="wide")

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
    h1, h2 { color: #692475 !important; }
    h3 { color: #82AB7D !important; }
    .guide-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Documentation & Help")

# Quick Start Guide
st.header("Quick Start Guide")
st.markdown("""
    <div style='background-color: #A47DAB22; padding: 1.5rem; border-radius: 5px; margin-bottom: 2rem;'>
        <h3 style='color: #692475; margin-top: 0;'>Getting Started</h3>
        <ol>
            <li>Prepare your microscopic images of mild steel samples</li>
            <li>Upload images for different time stages (NP, 1Y, 1YB, 5Y, 5YB)</li>
            <li>Click "Analyze Degradation" to process the images</li>
            <li>Review results and download the analysis report</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

# Image Requirements
st.header("Image Requirements")
st.markdown("""
    <div class='guide-section'>
        <h3>Recommended Image Specifications</h3>
        <ul>
            <li>Format: JPG, PNG, or JPEG</li>
            <li>Resolution: Minimum 1024x1024 pixels</li>
            <li>Consistent magnification across all samples</li>
            <li>Good focus and lighting</li>
            <li>Clean, dust-free surface</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Analysis Methods
st.header("Analysis Methods")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='guide-section'>
            <h3>Image Processing Steps</h3>
            <ol>
                <li><b>Grayscale Conversion:</b> Converts color image to grayscale</li>
                <li><b>CLAHE Enhancement:</b> Improves local contrast</li>
                <li><b>Adaptive Thresholding:</b> Identifies degraded regions</li>
                <li><b>Morphological Operations:</b> Removes noise and refines detection</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='guide-section'>
            <h3>Metrics Explained</h3>
            <ul>
                <li><b>Degradation %:</b> Percentage of surface area showing degradation</li>
                <li><b>Mean Intensity:</b> Average brightness level (0-255)</li>
                <li><b>Standard Intensity:</b> Variation in surface texture</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Best Practices
st.header("Best Practices")
st.markdown("""
    <div class='guide-section'>
        <h3>For Best Results</h3>
        <ul>
            <li>Use consistent imaging conditions for all samples</li>
            <li>Ensure proper sample preparation and cleaning</li>
            <li>Maintain same camera settings across all images</li>
            <li>Document any special conditions or treatments</li>
            <li>Regular calibration of microscope settings</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
# Troubleshooting
st.header("Troubleshooting")
st.markdown("""
    <div class='guide-section'>
        <h3>Common Issues</h3>
        <ol>
            <li><b>Poor Detection Results</b>
                <ul>
                    <li>Check image focus and lighting</li>
                    <li>Ensure proper sample cleaning</li>
                    <li>Try adjusting image contrast</li>
                </ul>
            </li>
            <li><b>Inconsistent Results</b>
                <ul>
                    <li>Verify consistent magnification</li>
                    <li>Check for proper sample preparation</li>
                    <li>Ensure similar lighting conditions</li>
                </ul>
            </li>
        </ol>
    </div>
""", unsafe_allow_html=True)
# Contact & Support
st.header("Contact & Support")
st.markdown("""
    <div style='background-color: #82AB7D22; padding: 1rem; border-radius: 5px;'>
        <h3 style='color: #692475; margin-top: 0;'>Need Help?</h3>
        <p>For technical support or questions, please contact:</p>
        <ul>
            <li>Email: support@mildsteel-analysis.com</li>
            <li>Technical Documentation: <a href="#">docs.mildsteel-analysis.com</a></li>
            <li>GitHub Repository: <a href="#">github.com/mildsteel-analysis</a></li>
        </ul>
    </div>
""", unsafe_allow_html=True) 