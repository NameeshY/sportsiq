"""
SportsIQ - Real-time NBA Analytics Dashboard
Main application file - Home page
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import time

# Add the parent directory to the Python path if running the file directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our utilities
from sportsiq.utils import setup_logging, get_logger, test_connection, execute_query

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

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .feature-header {
        font-size: 1.2rem;
        color: #1E88E5;
        font-weight: bold;
    }
    .card {
        border-radius: 5px;
        padding: 20px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        text-align: center;
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #616161;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.8rem;
        color: #9e9e9e;
    }
</style>
""", unsafe_allow_html=True)

def check_database():
    """Test the database connection and return status"""
    connection_status = test_connection()
    
    if connection_status:
        st.sidebar.success("✅ Database connected", icon="✅")
        module_logger.info("Database connection succeeded")
        return True
    else:
        st.sidebar.error("❌ Database not connected", icon="❌")
        module_logger.error("Database connection failed in the app")
        return False
    
def get_sample_stats():
    """Get sample statistics for display on the home page"""
    # Sample data (replace with real data from database when available)
    return {
        'total_players': 450,
        'total_teams': 30,
        'games_analyzed': 1230,
        'data_points': "1.2M+"
    }

def show_health_indicator(score, label):
    """Display a health indicator gauge chart"""
    colors = {
        'good': '#2E7D32',
        'medium': '#FF9800',
        'poor': '#C62828'
    }
    
    if score >= 70:
        color = colors['good']
        status = "Excellent"
    elif score >= 40:
        color = colors['medium']
        status = "Moderate"
    else:
        color = colors['poor']
        status = "Poor"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': label, 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': '#FFEBEE'},
                {'range': [40, 70], 'color': '#FFF9C4'},
                {'range': [70, 100], 'color': '#E8F5E9'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=25, b=10),
    )
    
    return fig, status

# Main content
def main():
    # App title and description
    st.markdown('<div class="main-header">🏀 SportsIQ NBA Analytics</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; font-size: 1.2rem; margin-bottom: 30px;">
        Real-time NBA analytics dashboard providing insights on player performance, 
        team statistics, and injury risk indicators.
        </div>
    """, unsafe_allow_html=True)
    
    # Check database connection
    db_connected = check_database()
    
    # Dashboard stats
    stats = get_sample_stats()
    
    # Display dashboard metrics
    st.markdown('<div class="sub-header">Dashboard Overview</div>', unsafe_allow_html=True)
    
    # Create columns for the metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">NBA Teams</div>
        </div>
        """.format(stats['total_teams']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Players Tracked</div>
        </div>
        """.format(stats['total_players']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Games Analyzed</div>
        </div>
        """.format(stats['games_analyzed']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Data Points</div>
        </div>
        """.format(stats['data_points']), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # System health indicators
    st.markdown('<div class="sub-header">System Health</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        db_score = 85 if db_connected else 20
        fig, status = show_health_indicator(db_score, "Database Status")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<div style='text-align: center;'><b>Status:</b> {status}</div>", unsafe_allow_html=True)
    
    with col2:
        # API health would come from real monitoring in production
        api_score = 78
        fig, status = show_health_indicator(api_score, "NBA API Status")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<div style='text-align: center;'><b>Status:</b> {status}</div>", unsafe_allow_html=True)
    
    with col3:
        # Data freshness would come from real monitoring in production
        freshness_score = 92
        fig, status = show_health_indicator(freshness_score, "Data Freshness")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<div style='text-align: center;'><b>Status:</b> {status}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features overview
    st.markdown('<div class="sub-header">Features</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-header">🔍 Player Performance Dashboard</div>', unsafe_allow_html=True)
        st.markdown("""
        - Compare multiple players across seasons or specific games
        - Display trends for points, efficiency, fouls, assists
        - Compute rolling averages and highlight statistical outliers
        - Visualize performance metrics with interactive charts
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-header">🏆 Optimal Lineup Analyzer</div>', unsafe_allow_html=True)
        st.markdown("""
        - Identify the most effective 5-player combinations
        - Filter by minimum minutes played together
        - Performance metrics include Net Rating, Offensive Rating, and Defensive Rating
        - Compare lineup efficiency across different time periods
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-header">⚠️ Injury Risk Indicator</div>', unsafe_allow_html=True)
        st.markdown("""
        - Calculate fatigue based on playing minutes, usage rate, and game frequency
        - Machine learning-based risk assessment
        - Visual indicators for injury risk levels
        - Track player workload over time
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-header">📊 Player Clustering & Game Prediction</div>', unsafe_allow_html=True)
        st.markdown("""
        - Machine learning algorithms to identify player archetypes
        - Visual representation of player clusters
        - Identify similar players based on statistical profiles
        - Predict game outcomes based on team performance data
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sample visualization
    st.markdown('<div class="sub-header">Sample Visualization</div>', unsafe_allow_html=True)
    
    # Sample data for visualization
    sample_data = {
        'Player': ['LeBron James', 'Kevin Durant', 'Stephen Curry', 
                  'Giannis Antetokounmpo', 'Nikola Jokic'],
        'Points': [27.5, 29.1, 28.7, 30.2, 25.3],
        'Assists': [7.9, 5.3, 6.1, 5.8, 9.2],
        'Rebounds': [8.5, 7.2, 5.4, 11.7, 12.1]
    }
    df = pd.DataFrame(sample_data)
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Player Stats Comparison", "Performance Radar"])
    
    with tab1:
        # Bar chart
        fig = px.bar(
            df, 
            x='Player', 
            y=['Points', 'Assists', 'Rebounds'],
            barmode='group',
            title="Key Statistics - Top Players",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(
            legend_title="Statistic",
            xaxis_title="",
            yaxis_title="Value",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Radar chart for comparing players
        categories = ['Points', 'Assists', 'Rebounds']
        
        fig = go.Figure()
        
        for i, player in enumerate(df['Player']):
            values = df.iloc[i, 1:].tolist()
            values.append(values[0])  # Close the loop
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],  # Add first value at end to close the polygon
                theta=categories + [categories[0]],  # Add first category at end
                fill='toself',
                name=player
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(df[['Points', 'Assists', 'Rebounds']].max()) * 1.1]
                )
            ),
            title="Player Performance Comparison",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add a note about the data
    st.info("Note: This is sample data for demonstration purposes. The dashboard uses real-time data from the NBA API when connected to the database.")
    
    # Footer
    st.markdown("<div class='footer'>© 2023 SportsIQ | Developed with ❤️ by the SportsIQ Team</div>", unsafe_allow_html=True)
    
    # Log page view
    module_logger.info("User viewed the Home page")

if __name__ == "__main__":
    module_logger.info("Running app directly")
    main()
