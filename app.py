"""
SportsIQ - Real-time NBA Analytics Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add the parent directory to the Python path if running the file directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our utilities
from sportsiq.utils import setup_logging, get_logger, test_connection

# Set up logging
logger = setup_logging()
module_logger = get_logger("app")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - NBA Analytics",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🏀 SportsIQ NBA Analytics")
st.markdown("""
    Real-time NBA analytics dashboard providing insights on player performance, 
    team statistics, and injury risk indicators.
""")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Home", "Player Dashboard", "Team Analysis", "Injury Risk", "About"]
)

# Test database connection
connection_status = test_connection()

# Display connection status
if connection_status:
    st.sidebar.success("✅ Database connected", icon="✅")
else:
    st.sidebar.error("❌ Database not connected", icon="❌")
    module_logger.error("Database connection failed in the app")

# Main content based on selected page
if page == "Home":
    st.header("Welcome to SportsIQ!")
    
    # Display some basic information about the app
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Features")
        st.markdown("""
        - Player performance metrics and trends
        - Team-level statistical analysis
        - Injury risk assessment
        - Historical data comparison
        - Real-time updates during games
        """)
    
    with col2:
        st.subheader("Getting Started")
        st.markdown("""
        1. Use the sidebar to navigate between different views
        2. Select players or teams to analyze
        3. Adjust filters for time periods and statistics
        4. Explore visualizations and insights
        """)
    
    # Sample visualization placeholder
    st.subheader("Sample Visualization")
    
    # Sample data (replace with real data later)
    sample_data = {
        'Player': ['LeBron James', 'Kevin Durant', 'Stephen Curry', 
                  'Giannis Antetokounmpo', 'Nikola Jokic'],
        'Points': [27.5, 29.1, 28.7, 30.2, 25.3],
        'Assists': [7.9, 5.3, 6.1, 5.8, 9.2],
        'Rebounds': [8.5, 7.2, 5.4, 11.7, 12.1]
    }
    df = pd.DataFrame(sample_data)
    
    # Create a radar chart for player comparison
    fig = px.line_polar(
        df, 
        r='Points', 
        theta='Player', 
        line_close=True,
        range_r=[20, 35],
        title="Points Per Game - Top Players"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Add a note about the data
    st.info("Note: This is sample data for demonstration purposes. The actual app will use real-time data from the NBA API.")

elif page == "Player Dashboard":
    st.header("Player Dashboard")
    st.write("This page will contain detailed player statistics and analysis.")
    
    # Placeholder for future implementation
    st.info("🚧 This feature is under development. Check back soon! 🚧")

elif page == "Team Analysis":
    st.header("Team Analysis")
    st.write("This page will contain team-level statistics and analysis.")
    
    # Placeholder for future implementation
    st.info("🚧 This feature is under development. Check back soon! 🚧")

elif page == "Injury Risk":
    st.header("Injury Risk Assessment")
    st.write("This page will provide injury risk indicators and analysis.")
    
    # Placeholder for future implementation
    st.info("🚧 This feature is under development. Check back soon! 🚧")

elif page == "About":
    st.header("About SportsIQ")
    st.write("Learn more about the SportsIQ project and team.")
    
    st.markdown("""
    ## About the Project
    
    SportsIQ is an advanced basketball analytics dashboard that provides real-time insights for NBA players and teams.
    The project combines data from various sources with machine learning models to provide predictive analytics.
    
    ## Technologies Used
    
    - **Streamlit**: For the interactive web application
    - **PostgreSQL**: For database management
    - **Pandas & NumPy**: For data manipulation
    - **Plotly & Matplotlib**: For data visualization
    - **Scikit-learn**: For machine learning models
    - **NBA API**: For real-time NBA data
    
    ## Project Team
    
    SportsIQ is developed as part of a data science project focusing on sports analytics and injury prediction.
    
    ## Contact
    
    For more information or to contribute to the project, please visit our GitHub repository.
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 SportsIQ | Developed with ❤️ by the SportsIQ Team")

# Log page view
module_logger.info(f"User viewed the {page} page")

if __name__ == "__main__":
    module_logger.info("Running app directly")
