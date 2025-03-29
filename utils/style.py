"""
SportsIQ - Style Utilities
Centralized CSS definitions for consistent styling across all pages
"""

def get_light_mode_css():
    """Return the CSS for forcing light mode across all pages"""
    return """
<style>
    /* Root elements */
    html, body, [class*="css"], [class*="st-"] {
        color: rgb(49, 51, 63) !important;
        background-color: white !important;
    }
    
    /* Force theme with !important */
    :root {
        --background-color: white !important;
        --text-color: rgb(49, 51, 63) !important;
        --secondary-background-color: #f8f9fa !important;
        --secondary-text-color: #71747c !important;
        --primary-color: #1E88E5 !important;
        --font: "Source Sans Pro", sans-serif !important;
    }
    
    /* Direct Streamlit element targeting */
    .stApp {
        background-color: white !important;
        color: rgb(49, 51, 63) !important;
    }
    
    /* Target all emotion cache classes that control theming */
    [class*="st-"], [class*="st-emotion-cache"], .st-emotion-cache-r421ms, 
    .st-emotion-cache-10trblm, .st-emotion-cache-16txtl3, .st-emotion-cache-1gulkj5, 
    .st-emotion-cache-e370rw, .st-emotion-cache-18ni7ap, .st-emotion-cache-uf99v8,
    .st-emotion-cache-6qob1r, .st-emotion-cache-ue6h4q, .st-emotion-cache-4z1n4l, 
    .st-emotion-cache-5rimss {
        background-color: white !important;
        color: rgb(49, 51, 63) !important;
    }
    
    /* Handle all widget types specifically */
    .stButton, .stTextInput, .stSelectbox, .stDateInput, .stNumberInput, .stSlider, 
    .stCheckbox, .stRadio, .stDataFrame, .stTable, .stMarkdown, .stText, .stTitle, 
    .stPlotlyChart, .stVegaLiteChart, .stImage, .stAlert, .stProgress, .stTabs, .stTab {
        color: rgb(49, 51, 63) !important;
        background-color: white !important;
    }
    
    /* Sidebar with stronger selectors */
    [data-testid="stSidebar"], .css-6qob1r, .css-ue6h4q, .css-4z1n4l, .css-5rimss,
    aside, aside div, .stSidebar, .stSidebarNav, .css-1544g2n {
        background-color: #f8f9fa !important;
        color: rgb(49, 51, 63) !important;
    }
    
    /* Headers and all text elements */
    h1, h2, h3, h4, h5, h6, p, div, span, .st-cp, .st-cx, .st-cy, .st-cz, .st-da, 
    .st-db, .st-dc, .st-dd, .st-de, .st-df, label, .stMarkdown {
        color: rgb(49, 51, 63) !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #f0f2f6 !important;
        color: rgb(49, 51, 63) !important;
    }

    /* Primary buttons */
    .stButton>button[data-baseweb="button"][kind="primary"] {
        background-color: #1E88E5 !important;
        color: white !important;
    }
    
    /* Code blocks - ensure they're visible in light mode */
    .stCodeBlock, pre, code {
        background-color: #f5f5f5 !important;
        color: #37474F !important;
    }
    
    /* Table elements with stronger selectors */
    .dataframe, th, td, [data-testid="stTable"] {
        background-color: white !important;
        color: rgb(49, 51, 63) !important;
        border-color: #e0e0e0 !important;
    }
    
    /* Ensure all plots have light backgrounds */
    .js-plotly-plot, .plot-container, .svg-container, [class*="highcharts"], 
    canvas, .plotly, svg {
        background-color: white !important;
        color: rgb(49, 51, 63) !important;
    }
    
    /* Force SVG elements to have proper colors in light mode */
    svg, path, line, circle, rect, polygon {
        stroke: currentColor !important;
        fill: currentColor !important;
    }
    
    /* Tabs container and indicator */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: rgb(49, 51, 63) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #1E88E5 !important;
    }
    
    /* Page content */
    section[data-testid="stSidebar"] + section, main {
        background-color: white !important;
    }
    
    /* Settings menu */
    button[kind="headerNoPadding"] {
        color: rgb(49, 51, 63) !important;
    }
    
    /* Images */
    img {
        background-color: transparent !important;
    }
    
    /* Plotly charts specifically */
    .plotly {
        background-color: white !important;
    }
    
    .plotly .main-svg {
        background-color: white !important;
    }
    
    /* SVG specific overrides for plots */
    .main-svg .bg {
        fill: white !important;
    }
    
    .svg-container {
        background-color: white !important;
    }
</style>
"""

def apply_light_mode():
    """Apply light mode CSS to the current Streamlit page"""
    import streamlit as st
    st.markdown(get_light_mode_css(), unsafe_allow_html=True) 