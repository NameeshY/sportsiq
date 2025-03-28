"""
SportsIQ - About Page
Provides information about the project, team, and technology stack
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
from sportsiq.utils import setup_logging, get_logger

# Set up logging
logger = setup_logging()
module_logger = get_logger("about")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - About",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .page-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #424242;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .tech-card {
        border-radius: 5px;
        padding: 1rem;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        text-align: center;
    }
    .tech-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .tech-name {
        font-weight: bold;
        font-size: 1.1rem;
    }
    .tech-desc {
        font-size: 0.9rem;
        color: #666;
    }
    .person-card {
        border-radius: 5px;
        padding: 1.5rem;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        text-align: center;
    }
    .about-section {
        border-radius: 5px;
        padding: 1.5rem;
        background-color: #f0f7ff;
        margin-bottom: 1.5rem;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.8rem;
        color: #9e9e9e;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def create_tech_usage_chart():
    """Create a bar chart showing tech stack usage"""
    tech_data = {
        "Technology": [
            "Streamlit", "PostgreSQL", "Pandas", "NumPy", 
            "Plotly", "Matplotlib", "Scikit-learn", "NBA API"
        ],
        "Usage": [100, 85, 95, 80, 90, 60, 75, 65],
        "Category": [
            "UI/Front-end", "Database", "Data Processing", "Data Processing", 
            "Visualization", "Visualization", "Machine Learning", "Data Source"
        ]
    }
    
    df = pd.DataFrame(tech_data)
    
    fig = px.bar(
        df, 
        x="Technology", 
        y="Usage", 
        color="Category",
        labels={"Usage": "Usage in Project (%)"},
        title="Technology Stack Utilization",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Usage (%)",
        template="plotly_white",
        legend_title="Category"
    )
    
    return fig

def main():
    st.markdown('<div class="page-title">About SportsIQ</div>', unsafe_allow_html=True)
    
    # Project overview
    st.markdown("""
    <div class="about-section">
        <h2>Project Overview</h2>
        <p>
            SportsIQ is an advanced basketball analytics dashboard that provides real-time insights for NBA teams and players.
            The project combines data from various sources with machine learning models to provide predictive analytics
            and visual representations of basketball data.
        </p>
        <p>
            Our mission is to transform raw basketball data into actionable insights that can be used by coaches, players,
            analysts, recruiters, and basketball enthusiasts to make informed decisions and gain deeper understanding of the game.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features
    st.markdown('<div class="section-title">Key Features</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        * **Player Performance Dashboard**
            * Track individual player statistics and trends
            * Compare multiple players across various metrics
            * Visualize performance with interactive charts
        
        * **Injury Risk Indicator**
            * Assess player fatigue and injury risk
            * Monitor workload and recovery metrics
            * Generate risk alerts based on predictive models
        """)
    
    with col2:
        st.markdown("""
        * **Team Analysis**
            * Analyze team performance metrics
            * Identify optimal lineup combinations
            * Compare team statistics across the league
        
        * **Game Prediction**
            * Predict game outcomes with machine learning
            * Analyze matchup strengths and weaknesses
            * Identify key factors influencing game results
        """)
    
    # Technology stack
    st.markdown('<div class="section-title">Technology Stack</div>', unsafe_allow_html=True)
    
    # Tech stack diagram
    tech_chart = create_tech_usage_chart()
    st.plotly_chart(tech_chart, use_container_width=True)
    
    # Tech stack details
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
        <div class="tech-card">
            <div class="tech-icon">📊</div>
            <div class="tech-name">Streamlit</div>
            <div class="tech-desc">Interactive web application framework</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🛢️</div>
            <div class="tech-name">PostgreSQL</div>
            <div class="tech-desc">Relational database management</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🐼</div>
            <div class="tech-name">Pandas</div>
            <div class="tech-desc">Data manipulation and analysis</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🧮</div>
            <div class="tech-name">NumPy</div>
            <div class="tech-desc">Scientific computing and arrays</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">📈</div>
            <div class="tech-name">Plotly</div>
            <div class="tech-desc">Interactive data visualizations</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">📉</div>
            <div class="tech-name">Matplotlib</div>
            <div class="tech-desc">Static data visualizations</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🤖</div>
            <div class="tech-name">Scikit-learn</div>
            <div class="tech-desc">Machine learning algorithms</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🏀</div>
            <div class="tech-name">NBA API</div>
            <div class="tech-desc">Official NBA data source</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data sources
    st.markdown('<div class="section-title">Data Sources</div>', unsafe_allow_html=True)
    
    st.markdown("""
    SportsIQ utilizes data from multiple sources to provide comprehensive analytics:
    
    * **NBA API**: Official statistics from the NBA, including play-by-play data, player and team stats
    * **Basketball Reference**: Historical data for long-term trend analysis
    * **Injury Reports**: Official NBA injury reports and player availability updates
    * **Advanced Metrics**: Proprietary calculations for advanced basketball analytics
    
    All data is regularly updated to ensure the latest information is available for analysis.
    """)
    
    # Implementation details
    st.markdown('<div class="section-title">Project Implementation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Data Pipeline
        
        * Data collection from NBA API and other sources
        * ETL processes for data cleaning and transformation
        * Storage in PostgreSQL database
        * Scheduled updates for real-time analytics
        
        ### Analytics Engine
        
        * Statistical analysis of player and team performance
        * Machine learning models for predictions
        * Advanced metrics calculation
        * Trend analysis and pattern recognition
        """)
    
    with col2:
        st.markdown("""
        ### Frontend Interface
        
        * Interactive dashboard with Streamlit
        * Dynamic visualization with Plotly
        * Responsive design for multiple devices
        * Customizable views and filters
        
        ### Deployment
        
        * Cloud-hosted application
        * Containerized for scalability
        * Version control with Git/GitHub
        * CI/CD pipeline for continuous deployment
        """)
    
    # Project team
    st.markdown('<div class="section-title">Project Team</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
        <div class="person-card">
            <img src="https://randomuser.me/api/portraits/men/32.jpg" width="150" style="border-radius: 50%;">
            <h3>David Johnson</h3>
            <p>Lead Data Scientist</p>
            <p style="font-size: 0.9rem;">Specializes in machine learning models and predictive analytics for sports data.</p>
        </div>
        <div class="person-card">
            <img src="https://randomuser.me/api/portraits/women/44.jpg" width="150" style="border-radius: 50%;">
            <h3>Sarah Chen</h3>
            <p>Full Stack Developer</p>
            <p style="font-size: 0.9rem;">Expert in Streamlit development and database integration for analytics platforms.</p>
        </div>
        <div class="person-card">
            <img src="https://randomuser.me/api/portraits/men/22.jpg" width="150" style="border-radius: 50%;">
            <h3>Michael Rodriguez</h3>
            <p>Sports Analytics Specialist</p>
            <p style="font-size: 0.9rem;">Former basketball analyst with extensive knowledge of NBA statistics and metrics.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Future roadmap
    st.markdown('<div class="section-title">Future Roadmap</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-section">
        <h3>Upcoming Features</h3>
        <ul>
            <li><strong>Advanced Player Comparison:</strong> More sophisticated tools for comparing players across different eras and playing styles</li>
            <li><strong>Shot Chart Analysis:</strong> Detailed visualization of shooting patterns and efficiency</li>
            <li><strong>Defensive Impact Metrics:</strong> Enhanced metrics for evaluating defensive contributions</li>
            <li><strong>Team Chemistry Indicators:</strong> Analysis of player combinations and their effectiveness</li>
            <li><strong>Mobile App:</strong> Native mobile application for on-the-go analytics</li>
            <li><strong>API Access:</strong> Public API for developers to integrate SportsIQ analytics into their applications</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact and feedback
    st.markdown('<div class="section-title">Contact & Feedback</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Contact Us
        
        * **Email**: info@sportsiq-analytics.com
        * **GitHub**: [github.com/NameeshY/sportsiq](https://github.com/NameeshY/sportsiq)
        * **Twitter**: [@SportsIQ_NBA](https://twitter.com)
        """)
    
    with col2:
        st.markdown("""
        ### Feedback
        
        We're constantly improving SportsIQ based on user feedback. 
        If you have suggestions, bug reports, or feature requests, 
        please submit them through our GitHub repository or contact us directly.
        """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        © 2023 SportsIQ | All data sourced from NBA and other public sources | 
        Not affiliated with the NBA or any basketball organization
    </div>
    """, unsafe_allow_html=True)
    
    # Log page view
    module_logger.info("User viewed About page")

if __name__ == "__main__":
    main() 