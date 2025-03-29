"""
SportsIQ - Player Dashboard
Analyze individual player performance metrics and statistics
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
import time
from datetime import datetime, timedelta
import logging

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
try:
    from sportsiq.utils.db_utils import test_connection, execute_query
    from sportsiq.utils.api_client import get_all_players
    from sportsiq.utils.style import apply_light_mode
except ImportError:
    # If import fails, create placeholder functions
    logging.basicConfig(level=logging.INFO)
    module_logger = logging.getLogger("player_dashboard")
    module_logger.warning("Could not import from sportsiq.utils, using placeholder functions")
    
    def test_connection():
        return True
    
    def execute_query(query, params=None):
        return []
    
    def get_all_players():
        return []
    
    def apply_light_mode():
        pass
else:
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    module_logger = logging.getLogger("player_dashboard")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - Player Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply light mode from central style utility
apply_light_mode()

# Custom CSS for this page only
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
    .card {
        border-radius: 5px;
        padding: 1.5rem;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 5px;
        background-color: #f5f5f5;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #616161;
    }
    .player-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .player-info {
        margin-left: 1rem;
    }
    .player-name {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
        padding: 0;
    }
    .player-team {
        font-size: 1.2rem;
        color: #616161;
        margin: 0;
        padding: 0;
    }
    .stat-comparison {
        padding: 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        background-color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Sample data functions (these would be replaced with real data from the database)
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_sample_players():
    """Return a sample list of NBA players"""
    return [
        {"id": 2544, "name": "LeBron James", "team": "Los Angeles Lakers", "position": "F"},
        {"id": 201939, "name": "Stephen Curry", "team": "Golden State Warriors", "position": "G"},
        {"id": 203954, "name": "Joel Embiid", "team": "Philadelphia 76ers", "position": "C"},
        {"id": 203507, "name": "Giannis Antetokounmpo", "team": "Milwaukee Bucks", "position": "F"},
        {"id": 201142, "name": "Kevin Durant", "team": "Phoenix Suns", "position": "F"},
        {"id": 1629027, "name": "Luka Doncic", "team": "Dallas Mavericks", "position": "G-F"},
        {"id": 1628369, "name": "Jayson Tatum", "team": "Boston Celtics", "position": "F"},
        {"id": 201566, "name": "Nikola Jokic", "team": "Denver Nuggets", "position": "C"},
        {"id": 1628983, "name": "Shai Gilgeous-Alexander", "team": "OKC Thunder", "position": "G"},
        {"id": 1627783, "name": "Donovan Mitchell", "team": "Cleveland Cavaliers", "position": "G"}
    ]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_player_game_stats(player_id, season="2022-23"):
    """Get player game statistics with generated sample data"""
    # This would be replaced with a database query in production
    seed = int(player_id) + hash(season) % 10000
    np.random.seed(seed)  # Use player ID and season as seed for consistency
    
    # Create 20 recent games
    # Use season to determine dates (if "2021-22", use dates from that season)
    season_year = int(season.split("-")[0])
    season_start = datetime(season_year, 10, 18)  # Season typically starts in October
    season_end = datetime(season_year+1, 4, 10)   # Regular season typically ends in April
    
    # Generate 20 game dates within the season
    total_season_days = (season_end - season_start).days
    game_intervals = total_season_days // 22  # 22 to ensure we get around 20 games
    
    dates = [season_start + timedelta(days=i*game_intervals) for i in range(20)]
    dates.reverse()  # Oldest to newest
    
    # Generate sample statistics with some randomness but realistic trends
    base_pts = np.random.randint(20, 30)
    base_ast = np.random.randint(4, 8)
    base_reb = np.random.randint(5, 10)
    
    stats = []
    for i, game_date in enumerate(dates):
        # Add some randomness to stats
        pts = max(0, base_pts + np.random.randint(-8, 9))
        ast = max(0, base_ast + np.random.randint(-3, 4))
        reb = max(0, base_reb + np.random.randint(-4, 5))
        fg_pct = round(np.random.uniform(0.35, 0.65), 3)
        fg3_pct = round(np.random.uniform(0.25, 0.55), 3)
        ft_pct = round(np.random.uniform(0.70, 0.95), 3)
        stl = max(0, np.random.randint(0, 4))
        blk = max(0, np.random.randint(0, 3))
        tov = max(0, np.random.randint(1, 6))
        min_played = max(20, np.random.randint(28, 38))
        plus_minus = np.random.randint(-15, 16)
        
        # Add trend effects (players get slightly better as season progresses)
        trend_factor = 1 + (i / 50)  # Small increase over time
        pts = int(pts * trend_factor)
        
        # Create opponent from list of teams
        teams = ["BOS", "MIA", "PHI", "TOR", "CHI", "CLE", "MIL", "NYK", "ATL", "CHA", 
                 "LAL", "GSW", "PHX", "LAC", "DEN", "MEM", "DAL", "POR", "UTA", "SAC"]
        opponent = teams[i % len(teams)]
        
        stats.append({
            "GAME_DATE": game_date,
            "MATCHUP": f"vs. {opponent}",
            "PTS": pts,
            "AST": ast,
            "REB": reb,
            "STL": stl,
            "BLK": blk,
            "TOV": tov,
            "FG_PCT": fg_pct,
            "FG3_PCT": fg3_pct,
            "FT_PCT": ft_pct,
            "MIN": min_played,
            "PLUS_MINUS": plus_minus,
            "SEASON": season
        })
    
    return pd.DataFrame(stats)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_player_season_stats(player_id):
    """Get player season statistics with generated sample data"""
    # This would be replaced with a database query in production
    np.random.seed(player_id)  # Use player ID as seed for consistency
    
    # Create last 3 seasons
    current_year = datetime.now().year
    seasons = [f"{year-1}-{str(year)[2:]}" for year in range(current_year-2, current_year+1)]
    
    # Base stats with some randomness
    base_pts = np.random.randint(18, 28)
    base_ast = np.random.randint(4, 8)
    base_reb = np.random.randint(4, 10)
    
    stats = []
    for i, season in enumerate(seasons):
        # Use both player ID and season for seed
        seed = int(player_id) + hash(season) % 10000
        np.random.seed(seed)
        
        # Add some randomness to stats but keep them relatively consistent across seasons
        pts = max(0, base_pts + np.random.randint(-3, 4))
        ast = max(0, base_ast + np.random.randint(-1, 2))
        reb = max(0, base_reb + np.random.randint(-2, 3))
        
        # Slight improvement trend over seasons
        trend_factor = 1 + (i / 20)  # Small increase over time
        pts = round(pts * trend_factor, 1)
        ast = round(ast * trend_factor, 1)
        reb = round(reb * trend_factor, 1)
        
        # Other stats
        fg_pct = round(np.random.uniform(0.44, 0.54), 3)
        fg3_pct = round(np.random.uniform(0.34, 0.42), 3)
        ft_pct = round(np.random.uniform(0.75, 0.90), 3)
        stl = round(np.random.uniform(0.7, 1.8), 1)
        blk = round(np.random.uniform(0.5, 1.5), 1)
        tov = round(np.random.uniform(1.8, 3.5), 1)
        min_played = round(np.random.uniform(28, 36), 1)
        games = np.random.randint(65, 82)
        
        stats.append({
            "SEASON": season,
            "GAMES": games,
            "PTS": pts,
            "AST": ast,
            "REB": reb,
            "STL": stl,
            "BLK": blk,
            "TOV": tov,
            "FG_PCT": fg_pct,
            "FG3_PCT": fg3_pct,
            "FT_PCT": ft_pct,
            "MIN": min_played,
            "PER": round(np.random.uniform(15, 25), 1),  # Player Efficiency Rating
            "TS_PCT": round(np.random.uniform(0.55, 0.65), 3),  # True Shooting %
            "USG_PCT": round(np.random.uniform(24, 33), 1)  # Usage Percentage
        })
    
    return pd.DataFrame(stats)

def create_performance_line_chart(player_stats, stat_column, title=None, rolling_window=5):
    """Create a line chart for player performance over time"""
    # Sort by date
    player_stats = player_stats.sort_values('GAME_DATE')
    
    # Create figure
    fig = go.Figure()
    
    # Add stat line
    fig.add_trace(
        go.Scatter(
            x=player_stats['GAME_DATE'],
            y=player_stats[stat_column],
            mode='lines+markers',
            name=stat_column,
            line=dict(color='#1E88E5', width=3),
            marker=dict(size=8)
        )
    )
    
    # Add rolling average if specified
    if rolling_window and len(player_stats) >= rolling_window:
        rolling_avg = player_stats[stat_column].rolling(window=rolling_window, min_periods=1).mean()
        fig.add_trace(
            go.Scatter(
                x=player_stats['GAME_DATE'],
                y=rolling_avg,
                mode='lines',
                name=f'{rolling_window}-Game Rolling Avg',
                line=dict(dash='dash', color='#FFA000', width=2)
            )
        )
    
    # Add season average line
    season_avg = player_stats[stat_column].mean()
    fig.add_trace(
        go.Scatter(
            x=[player_stats['GAME_DATE'].min(), player_stats['GAME_DATE'].max()],
            y=[season_avg, season_avg],
            mode='lines',
            name='Season Average',
            line=dict(dash='dot', color='#4CAF50', width=2)
        )
    )
    
    # Set title
    if title:
        fig.update_layout(title=title)
    else:
        fig.update_layout(title=f'{stat_column} Over Time')
    
    # Set layout
    fig.update_layout(
        xaxis_title='Game Date',
        yaxis_title=stat_column,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_radar_chart(player_stats, stats_columns, title=None):
    """Create a radar chart for player statistics"""
    # Calculate mean values for each stat
    stat_means = [player_stats[col].mean() for col in stats_columns]
    
    # Normalize values between 0 and 1 for presentation
    max_vals = {'PTS': 40, 'AST': 15, 'REB': 20, 'STL': 5, 'BLK': 5, 'TOV': 5, 
                'FG_PCT': 1, 'FG3_PCT': 1, 'FT_PCT': 1, 'PLUS_MINUS': 30}
    
    normalized_stats = []
    for i, col in enumerate(stats_columns):
        if col in max_vals:
            normalized_stats.append(min(1, max(0, stat_means[i] / max_vals[col])))
        else:
            normalized_stats.append(min(1, max(0, stat_means[i] / 40)))  # Default normalization
    
    # Add first value at the end to close the radar
    normalized_stats.append(normalized_stats[0])
    stat_labels = stats_columns.copy()
    stat_labels.append(stat_labels[0])
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatterpolar(
            r=normalized_stats,
            theta=stat_labels,
            fill='toself',
            line=dict(color='#1E88E5', width=3),
            name='Performance'
        )
    )
    
    # Add reference line at 0.5 (average performance)
    fig.add_trace(
        go.Scatterpolar(
            r=[0.5] * len(stat_labels),
            theta=stat_labels,
            fill=None,
            line=dict(color='#9E9E9E', width=1, dash='dash'),
            name='League Average'
        )
    )
    
    # Set layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=['0%', '25%', '50%', '75%', '100%']
            )
        ),
        title=title or 'Player Performance Radar',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_shooting_chart(player_stats, title=None):
    """Create a chart to visualize shooting percentages"""
    # Sort by date
    player_stats = player_stats.sort_values('GAME_DATE')
    
    # Create subplot with 3 rows
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Field Goal %", "3-Point %", "Free Throw %"),
        shared_xaxes=True,
        vertical_spacing=0.1
    )
    
    # Add field goal percentage
    fig.add_trace(
        go.Scatter(
            x=player_stats['GAME_DATE'],
            y=player_stats['FG_PCT'] * 100,  # Convert to percentage
            mode='lines+markers',
            name='FG%',
            line=dict(color='#1E88E5')
        ),
        row=1, col=1
    )
    
    # Add 3-point percentage
    fig.add_trace(
        go.Scatter(
            x=player_stats['GAME_DATE'],
            y=player_stats['FG3_PCT'] * 100,  # Convert to percentage
            mode='lines+markers',
            name='3P%',
            line=dict(color='#FFA000')
        ),
        row=2, col=1
    )
    
    # Add free throw percentage
    fig.add_trace(
        go.Scatter(
            x=player_stats['GAME_DATE'],
            y=player_stats['FT_PCT'] * 100,  # Convert to percentage
            mode='lines+markers',
            name='FT%',
            line=dict(color='#4CAF50')
        ),
        row=3, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        title=title or 'Shooting Percentages',
        template='plotly_white',
        showlegend=False,
        hovermode='x unified'
    )
    
    # Update y-axes to show percentages
    fig.update_yaxes(range=[0, 100], ticksuffix='%')
    
    return fig

def create_stat_distribution_chart(player_stats, stat_column, title=None):
    """Create a histogram to show the distribution of a statistic"""
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(
        go.Histogram(
            x=player_stats[stat_column],
            nbinsx=10,
            marker_color='#1E88E5',
            opacity=0.7,
            name=stat_column
        )
    )
    
    # Add mean line
    mean_value = player_stats[stat_column].mean()
    fig.add_vline(
        x=mean_value,
        line_dash="dash",
        line_color="#FF5722",
        annotation_text=f"Mean: {mean_value:.1f}",
        annotation_position="top right"
    )
    
    # Update layout
    fig.update_layout(
        title=title or f'{stat_column} Distribution',
        xaxis_title=stat_column,
        yaxis_title='Frequency',
        template='plotly_white'
    )
    
    return fig

def get_performance_insights(player_stats, player_name):
    """Generate insights based on player statistics"""
    insights = []
    
    # Check last 5 games performance
    last_5_games = player_stats.sort_values('GAME_DATE', ascending=False).head(5)
    last_5_pts_avg = last_5_games['PTS'].mean()
    season_pts_avg = player_stats['PTS'].mean()
    
    if last_5_pts_avg > season_pts_avg * 1.15:
        insights.append(f"🔥 {player_name} is on fire! Averaging {last_5_pts_avg:.1f} points in the last 5 games, which is {((last_5_pts_avg / season_pts_avg) - 1) * 100:.1f}% above their season average.")
    elif last_5_pts_avg < season_pts_avg * 0.85:
        insights.append(f"📉 {player_name} is in a scoring slump, averaging only {last_5_pts_avg:.1f} points in the last 5 games, which is {(1 - (last_5_pts_avg / season_pts_avg)) * 100:.1f}% below their season average.")
    
    # Check for consistency
    pts_std = player_stats['PTS'].std()
    pts_mean = player_stats['PTS'].mean()
    pts_cv = pts_std / pts_mean  # Coefficient of variation
    
    if pts_cv < 0.2:
        insights.append(f"📊 {player_name} shows remarkable consistency in scoring, with a standard deviation of only {pts_std:.1f} points.")
    elif pts_cv > 0.4:
        insights.append(f"📊 {player_name}'s scoring has been inconsistent, with a high standard deviation of {pts_std:.1f} points.")
    
    # Check for best and worst games
    best_game = player_stats.loc[player_stats['PTS'].idxmax()]
    worst_game = player_stats.loc[player_stats['PTS'].idxmin()]
    
    insights.append(f"🌟 Best scoring game: {best_game['PTS']} points against {best_game['MATCHUP']} on {best_game['GAME_DATE'].strftime('%b %d, %Y')}.")
    insights.append(f"⬇️ Lowest scoring game: {worst_game['PTS']} points against {worst_game['MATCHUP']} on {worst_game['GAME_DATE'].strftime('%b %d, %Y')}.")
    
    # Check shooting percentages
    fg_pct_avg = player_stats['FG_PCT'].mean() * 100
    fg3_pct_avg = player_stats['FG3_PCT'].mean() * 100
    
    if fg_pct_avg > 50:
        insights.append(f"🎯 {player_name} has been highly efficient, shooting {fg_pct_avg:.1f}% from the field this season.")
    
    if fg3_pct_avg > 38:
        insights.append(f"🎯 {player_name} has been an excellent 3-point shooter, hitting {fg3_pct_avg:.1f}% from beyond the arc.")
    elif fg3_pct_avg < 32:
        insights.append(f"🎯 {player_name} has struggled from 3-point range, shooting only {fg3_pct_avg:.1f}%.")
    
    return insights

def main():
    st.markdown('<div class="page-title">Player Performance Dashboard</div>', unsafe_allow_html=True)
    
    # Database connection status
    db_connected = test_connection()
    
    if not db_connected:
        st.warning("⚠️ Database connection failed. Using sample data for demonstration.", icon="⚠️")
    
    # Player selection sidebar
    st.sidebar.header("Player Selection")
    
    # Get player list (from database or sample)
    players = get_sample_players()
    player_options = [p["name"] for p in players]
    
    # Select player
    selected_player_name = st.sidebar.selectbox("Select Player", player_options)
    selected_player = next((p for p in players if p["name"] == selected_player_name), None)
    
    if not selected_player:
        st.error("No player selected. Please select a player from the sidebar.")
        return
    
    # Display season selection
    current_year = datetime.now().year
    seasons = [f"{year-1}-{str(year)[2:]}" for year in range(current_year-2, current_year+1)]
    
    # Check if season has changed
    if 'previous_season' not in st.session_state:
        st.session_state.previous_season = seasons[-1]  # Default to most recent season
        
    selected_season = st.sidebar.selectbox("Select Season", seasons, index=len(seasons)-1)
    
    # Add a button to clear cache and reload data
    if st.sidebar.button("Refresh Data"):
        # Clear cached data
        get_player_game_stats.clear()
        get_player_season_stats.clear()
        st.sidebar.success("Data cache cleared! New data will be loaded.")
    
    # Check if season changed and clear cache automatically
    if st.session_state.previous_season != selected_season:
        get_player_game_stats.clear()
        get_player_season_stats.clear()
        st.session_state.previous_season = selected_season
    
    # Statistic selection for charts
    stat_options = ["PTS", "AST", "REB", "STL", "BLK", "TOV", "PLUS_MINUS"]
    selected_stat = st.sidebar.selectbox("Select Statistic for Analysis", stat_options, index=0)
    
    # Visualization settings
    st.sidebar.header("Visualization Settings")
    show_rolling_avg = st.sidebar.checkbox("Show Rolling Average", value=True)
    rolling_window = st.sidebar.slider("Rolling Average Window", min_value=3, max_value=10, value=5) if show_rolling_avg else None
    
    # Load player data
    with st.spinner("Loading player data..."):
        # This would be replaced with database queries in production
        player_game_stats = get_player_game_stats(selected_player["id"], selected_season)
        player_season_stats = get_player_season_stats(selected_player["id"])
    
    # Player header section
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Player image (would be replaced with actual player images in production)
        st.image(f"https://cdn.nba.com/headshots/nba/latest/1040x760/{selected_player['id']}.png", 
                width=200, caption=selected_player_name)
    
    with col2:
        # Player info and current season stats
        current_season_stats = player_season_stats.iloc[-1]  # Most recent season
        
        st.markdown(f"""
        <div class='card'>
            <h3>{selected_player_name}</h3>
            <p>{selected_player['team']} | Position: {selected_player['position']}</p>
            <p>Season: {selected_season}</p>
            <hr>
            <div style='display: flex; justify-content: space-between;'>
                <div class='stat-card'>
                    <div class='stat-value'>{current_season_stats['PTS']}</div>
                    <div class='stat-label'>PPG</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-value'>{current_season_stats['REB']}</div>
                    <div class='stat-label'>RPG</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-value'>{current_season_stats['AST']}</div>
                    <div class='stat-label'>APG</div>
                </div>
                <div class='stat-card'>
                    <div class='stat-value'>{current_season_stats['PER']}</div>
                    <div class='stat-label'>PER</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance insights
    st.markdown('<div class="section-title">Performance Insights</div>', unsafe_allow_html=True)
    
    insights = get_performance_insights(player_game_stats, selected_player_name)
    
    for insight in insights:
        st.markdown(f"<div class='highlight'>{insight}</div>", unsafe_allow_html=True)
    
    # Performance Trend Tab
    st.markdown('<div class="section-title">Performance Trends</div>', unsafe_allow_html=True)
    
    performance_tabs = st.tabs(["Scoring", "Efficiency", "All-Around Game"])
    
    with performance_tabs[0]:
        # Points trend
        st.plotly_chart(
            create_performance_line_chart(
                player_game_stats, 
                'PTS', 
                f"{selected_player_name} - Points Trend", 
                rolling_window
            ),
            use_container_width=True
        )
        
        # Points distribution
        st.plotly_chart(
            create_stat_distribution_chart(
                player_game_stats, 
                'PTS', 
                f"{selected_player_name} - Points Distribution"
            ),
            use_container_width=True
        )
    
    with performance_tabs[1]:
        # Shooting percentages
        st.plotly_chart(
            create_shooting_chart(
                player_game_stats, 
                f"{selected_player_name} - Shooting Efficiency"
            ),
            use_container_width=True
        )
        
        # Efficiency metrics by game
        st.plotly_chart(
            create_performance_line_chart(
                player_game_stats, 
                'PLUS_MINUS', 
                f"{selected_player_name} - Plus/Minus", 
                rolling_window
            ),
            use_container_width=True
        )
    
    with performance_tabs[2]:
        # Radar chart for all-around game
        st.plotly_chart(
            create_radar_chart(
                player_game_stats, 
                ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT'], 
                f"{selected_player_name} - Performance Profile"
            ),
            use_container_width=True
        )
        
        # Selected stat trend
        if selected_stat not in ['PTS', 'PLUS_MINUS']:  # Don't show duplicates
            st.plotly_chart(
                create_performance_line_chart(
                    player_game_stats, 
                    selected_stat, 
                    f"{selected_player_name} - {selected_stat} Trend", 
                    rolling_window
                ),
                use_container_width=True
            )
    
    # Season comparison
    st.markdown('<div class="section-title">Season Comparison</div>', unsafe_allow_html=True)
    
    # Season stats table
    st.dataframe(
        player_season_stats[['SEASON', 'GAMES', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'PER']],
        use_container_width=True,
        hide_index=True
    )
    
    # Season comparison chart
    season_stats = player_season_stats[['SEASON', 'PTS', 'AST', 'REB']]
    season_stats_melted = pd.melt(season_stats, id_vars=['SEASON'], value_vars=['PTS', 'AST', 'REB'])
    
    fig = px.bar(
        season_stats_melted, 
        x='SEASON', 
        y='value', 
        color='variable',
        barmode='group',
        labels={'value': 'Average', 'variable': 'Statistic'},
        title=f"{selected_player_name} - Season Comparison",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Log page view
    module_logger.info(f"User viewed Player Dashboard for {selected_player_name}")

if __name__ == "__main__":
    main() 