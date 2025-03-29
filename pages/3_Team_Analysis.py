"""
SportsIQ - Team Analysis
Analyze team performance metrics and statistics
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import logging
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
try:
    from sportsiq.utils.db_utils import test_connection, execute_query
    from sportsiq.utils.api_client import get_all_teams
    from sportsiq.utils.style import apply_light_mode
except ImportError:
    # If import fails, create placeholder functions
    logging.basicConfig(level=logging.INFO)
    module_logger = logging.getLogger("team_analysis")
    module_logger.warning("Could not import from sportsiq.utils, using placeholder functions")
    
    def test_connection():
        return True
    
    def execute_query(query, params=None):
        return []
    
    def get_all_teams():
        return []
    
    def apply_light_mode():
        pass
else:
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    module_logger = logging.getLogger("team_analysis")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - Team Analysis",
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
    .team-section {
        margin-top: 2rem;
    }
    .rating-good {
        color: #388E3C;
        font-weight: bold;
    }
    .rating-average {
        color: #FFA000;
        font-weight: bold;
    }
    .rating-poor {
        color: #D32F2F;
        font-weight: bold;
    }
    .team-logo {
        text-align: center;
        margin-bottom: 1rem;
    }
    .player-row {
        padding: 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        background-color: #f0f0f0;
    }
    .lineup-card {
        border-radius: 5px;
        padding: 1rem;
        background-color: #f0f0f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sample data functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_sample_teams():
    """Return a sample list of NBA teams"""
    return [
        {"id": 1610612738, "name": "Boston Celtics", "abbr": "BOS", "conference": "East", "division": "Atlantic"},
        {"id": 1610612751, "name": "Brooklyn Nets", "abbr": "BKN", "conference": "East", "division": "Atlantic"},
        {"id": 1610612752, "name": "New York Knicks", "abbr": "NYK", "conference": "East", "division": "Atlantic"},
        {"id": 1610612755, "name": "Philadelphia 76ers", "abbr": "PHI", "conference": "East", "division": "Atlantic"},
        {"id": 1610612761, "name": "Toronto Raptors", "abbr": "TOR", "conference": "East", "division": "Atlantic"},
        {"id": 1610612741, "name": "Chicago Bulls", "abbr": "CHI", "conference": "East", "division": "Central"},
        {"id": 1610612739, "name": "Cleveland Cavaliers", "abbr": "CLE", "conference": "East", "division": "Central"},
        {"id": 1610612765, "name": "Detroit Pistons", "abbr": "DET", "conference": "East", "division": "Central"},
        {"id": 1610612754, "name": "Indiana Pacers", "abbr": "IND", "conference": "East", "division": "Central"},
        {"id": 1610612749, "name": "Milwaukee Bucks", "abbr": "MIL", "conference": "East", "division": "Central"},
        {"id": 1610612737, "name": "Atlanta Hawks", "abbr": "ATL", "conference": "East", "division": "Southeast"},
        {"id": 1610612766, "name": "Charlotte Hornets", "abbr": "CHA", "conference": "East", "division": "Southeast"},
        {"id": 1610612748, "name": "Miami Heat", "abbr": "MIA", "conference": "East", "division": "Southeast"},
        {"id": 1610612753, "name": "Orlando Magic", "abbr": "ORL", "conference": "East", "division": "Southeast"},
        {"id": 1610612764, "name": "Washington Wizards", "abbr": "WAS", "conference": "East", "division": "Southeast"},
        {"id": 1610612743, "name": "Denver Nuggets", "abbr": "DEN", "conference": "West", "division": "Northwest"},
        {"id": 1610612750, "name": "Minnesota Timberwolves", "abbr": "MIN", "conference": "West", "division": "Northwest"},
        {"id": 1610612760, "name": "Oklahoma City Thunder", "abbr": "OKC", "conference": "West", "division": "Northwest"},
        {"id": 1610612757, "name": "Portland Trail Blazers", "abbr": "POR", "conference": "West", "division": "Northwest"},
        {"id": 1610612762, "name": "Utah Jazz", "abbr": "UTA", "conference": "West", "division": "Northwest"},
        {"id": 1610612744, "name": "Golden State Warriors", "abbr": "GSW", "conference": "West", "division": "Pacific"},
        {"id": 1610612746, "name": "LA Clippers", "abbr": "LAC", "conference": "West", "division": "Pacific"},
        {"id": 1610612747, "name": "Los Angeles Lakers", "abbr": "LAL", "conference": "West", "division": "Pacific"},
        {"id": 1610612756, "name": "Phoenix Suns", "abbr": "PHX", "conference": "West", "division": "Pacific"},
        {"id": 1610612758, "name": "Sacramento Kings", "abbr": "SAC", "conference": "West", "division": "Pacific"},
        {"id": 1610612742, "name": "Dallas Mavericks", "abbr": "DAL", "conference": "West", "division": "Southwest"},
        {"id": 1610612745, "name": "Houston Rockets", "abbr": "HOU", "conference": "West", "division": "Southwest"},
        {"id": 1610612763, "name": "Memphis Grizzlies", "abbr": "MEM", "conference": "West", "division": "Southwest"},
        {"id": 1610612740, "name": "New Orleans Pelicans", "abbr": "NOP", "conference": "West", "division": "Southwest"},
        {"id": 1610612759, "name": "San Antonio Spurs", "abbr": "SAS", "conference": "West", "division": "Southwest"}
    ]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_team_stats(team_id, season="2022-23"):
    """Generate sample statistics for a team"""
    # Use both team ID and season as seed for consistency
    seed = int(team_id) + hash(season) % 10000
    np.random.seed(seed)
    
    # Basic stats
    win_pct = np.random.uniform(0.25, 0.75)
    wins = int(82 * win_pct)
    losses = 82 - wins
    
    # Offensive and defensive ratings
    # Better team = higher win percentage = better ratings generally
    ortg_base = 105 + (win_pct - 0.5) * 20
    drtg_base = 110 - (win_pct - 0.5) * 20
    
    # Add some randomness
    ortg = ortg_base + np.random.uniform(-3, 3)
    drtg = drtg_base + np.random.uniform(-3, 3)
    net_rtg = ortg - drtg
    
    # Points per game (related to offensive rating)
    pts_pg = ortg / 1.1 + np.random.uniform(-2, 2)
    opp_pts_pg = drtg / 1.1 + np.random.uniform(-2, 2)
    
    # Shooting percentages
    fg_pct = np.random.uniform(0.44, 0.49)
    fg3_pct = np.random.uniform(0.33, 0.38)
    ft_pct = np.random.uniform(0.75, 0.82)
    
    # Other basic stats
    reb_pg = np.random.uniform(40, 50)
    ast_pg = np.random.uniform(22, 30)
    stl_pg = np.random.uniform(6, 10)
    blk_pg = np.random.uniform(4, 7)
    to_pg = np.random.uniform(12, 16)
    
    # Advanced stats
    ts_pct = np.random.uniform(0.54, 0.60)
    efg_pct = np.random.uniform(0.50, 0.56)
    ast_ratio = np.random.uniform(16, 20)
    to_ratio = np.random.uniform(12, 16)
    reb_pct = np.random.uniform(48, 52)
    pace = np.random.uniform(95, 103)
    
    return {
        "WINS": wins,
        "LOSSES": losses,
        "WIN_PCT": win_pct,
        "PTS_PG": pts_pg,
        "OPP_PTS_PG": opp_pts_pg,
        "ORTG": ortg,
        "DRTG": drtg,
        "NET_RTG": net_rtg,
        "FG_PCT": fg_pct,
        "FG3_PCT": fg3_pct,
        "FT_PCT": ft_pct,
        "REB_PG": reb_pg,
        "AST_PG": ast_pg,
        "STL_PG": stl_pg,
        "BLK_PG": blk_pg,
        "TO_PG": to_pg,
        "TS_PCT": ts_pct,
        "EFG_PCT": efg_pct,
        "AST_RATIO": ast_ratio,
        "TO_RATIO": to_ratio,
        "REB_PCT": reb_pct,
        "PACE": pace,
        "SEASON": season
    }

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_team_players(team_id, season="2022-23"):
    """Generate sample players for a team"""
    # Use both team ID and season as seed for consistency
    seed = int(team_id) + hash(season) % 10000
    np.random.seed(seed)
    
    # Number of players to generate
    num_players = 15
    
    # Player positions
    positions = ["PG", "SG", "SF", "PF", "C"]
    
    # Generate player data
    players = []
    
    for i in range(num_players):
        # Basic player info
        player_id = team_id * 100 + i
        position = positions[min(i // 3, 4)]  # Distribute positions
        
        # Generate player statistics based on position and role
        if i < 5:  # Starters
            min_pg = np.random.uniform(25, 32)
            pts_pg = np.random.uniform(12, 24)
            reb_pg = np.random.uniform(3, 10)
            ast_pg = np.random.uniform(2, 7)
        elif i < 10:  # Rotation players
            min_pg = np.random.uniform(15, 24)
            pts_pg = np.random.uniform(6, 14)
            reb_pg = np.random.uniform(2, 6)
            ast_pg = np.random.uniform(1, 4)
        else:  # End of bench
            min_pg = np.random.uniform(5, 12)
            pts_pg = np.random.uniform(2, 8)
            reb_pg = np.random.uniform(1, 3)
            ast_pg = np.random.uniform(0.5, 2)
        
        # Adjust stats based on position
        if position in ["PG", "SG"]:
            ast_pg *= 1.5
            reb_pg *= 0.8
        elif position == "C":
            reb_pg *= 1.5
            ast_pg *= 0.6
            
        # Other stats
        stl_pg = np.random.uniform(0.3, 1.5)
        blk_pg = np.random.uniform(0.1, 1.0)
        if position == "C":
            blk_pg *= 2.0
        
        to_pg = np.random.uniform(0.5, 2.5)
        fg_pct = np.random.uniform(0.40, 0.54)
        fg3_pct = np.random.uniform(0.32, 0.42)
        ft_pct = np.random.uniform(0.70, 0.88)
        
        # Player names (random but consistent for given ID)
        first_names = ["James", "Michael", "Chris", "Kevin", "Anthony", "Stephen", "Russell", "LeBron", 
                      "Damian", "Jayson", "Luka", "Devin", "Trae", "Joel", "Giannis", "Nikola", "Jimmy"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Thomas", 
                     "Wilson", "Taylor", "Anderson", "Harris", "Moore", "Martin", "Jackson", "Thompson", 
                     "White", "Lopez", "Lee", "Gonzalez", "Rodriguez", "Lewis", "Walker", "Hall", 
                     "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson", 
                     "Carter", "Mitchell", "Parker", "Collins", "Edwards", "Stewart", "Morris", "Murphy"]
        
        # Use player ID to get consistent but varied names
        first_name_idx = player_id % len(first_names)
        last_name_idx = (player_id * 3) % len(last_names)
        
        first_name = first_names[first_name_idx]
        last_name = last_names[last_name_idx]
        
        players.append({
            "PLAYER_ID": player_id,
            "PLAYER_NAME": f"{first_name} {last_name}",
            "POSITION": position,
            "MIN": min_pg,
            "PTS": pts_pg,
            "REB": reb_pg,
            "AST": ast_pg,
            "STL": stl_pg,
            "BLK": blk_pg,
            "TO": to_pg,
            "FG_PCT": fg_pct,
            "FG3_PCT": fg3_pct,
            "FT_PCT": ft_pct,
            "STATUS": "Active" if i < 13 else ("Injured" if i == 13 else "G-League"),
            "SEASON": season
        })
    
    return pd.DataFrame(players)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_team_lineups(team_id, season="2022-23"):
    """Generate sample lineup statistics for a team"""
    # Use both team ID and season as seed for consistency
    seed = int(team_id) + hash(season) % 10000
    np.random.seed(seed)
    
    # Get team players to use in lineups
    players_df = get_team_players(team_id, season)
    players = players_df.head(10).to_dict('records')  # Use top 10 players
    
    # Generate various 5-player combinations
    num_lineups = 12
    lineups = []
    
    for i in range(num_lineups):
        # For the first lineup, use the top 5 players (starters)
        if i == 0:
            lineup_players = players[:5]
        else:
            # For other lineups, create different combinations
            # Ensure some overlap with starters but also variety
            starters_count = max(1, min(4, np.random.randint(2, 5)))
            bench_count = 5 - starters_count
            
            starter_indices = np.random.choice(5, starters_count, replace=False)
            bench_indices = np.random.choice(range(5, 10), bench_count, replace=False)
            
            lineup_players = [players[i] for i in starter_indices] + [players[i] for i in bench_indices]
        
        # Generate minutes played (more for starters)
        minutes = 500 if i == 0 else max(50, np.random.normal(200, 100))
        
        # Generate lineup's offensive and defensive ratings
        # Starters usually better, but some bench units can be specialized
        if i == 0:  # Starters
            ortg = np.random.uniform(110, 118)
            drtg = np.random.uniform(107, 115)
        elif i < 3:  # Common bench units
            ortg = np.random.uniform(108, 115)
            drtg = np.random.uniform(108, 116)
        else:  # Less common lineups
            ortg = np.random.uniform(105, 115)
            drtg = np.random.uniform(107, 118)
        
        # Calculate net rating
        net_rtg = ortg - drtg
        
        # Create lineup name from player last names
        lineup_name = " - ".join([p["PLAYER_NAME"].split()[-1] for p in lineup_players])
        
        # Generate other lineup metrics
        fg_pct = np.random.uniform(0.44, 0.49)
        fg3_pct = np.random.uniform(0.34, 0.40)
        ast_ratio = np.random.uniform(15, 21)
        reb_pct = np.random.uniform(47, 53)
        
        lineups.append({
            "LINEUP_ID": i + 1,
            "LINEUP": lineup_name,
            "PLAYERS": [p["PLAYER_NAME"] for p in lineup_players],
            "MINUTES": minutes,
            "ORTG": ortg,
            "DRTG": drtg,
            "NET_RTG": net_rtg,
            "FG_PCT": fg_pct,
            "FG3_PCT": fg3_pct,
            "AST_RATIO": ast_ratio,
            "REB_PCT": reb_pct,
            "SEASON": season
        })
    
    return pd.DataFrame(lineups)

def create_team_rankings_chart(team_name, team_stats):
    """Create a horizontal bar chart showing team rankings"""
    # Create sample data with rankings for all teams
    all_teams = get_sample_teams()
    ranking_data = []
    
    # Metrics to show rankings for
    metrics = {
        "NET_RTG": "Net Rating", 
        "ORTG": "Offensive Rating", 
        "DRTG": "Defensive Rating",
        "PTS_PG": "Points Per Game",
        "FG3_PCT": "3PT Percentage",
        "AST_PG": "Assists Per Game"
    }
    
    # Create consistent but realistic rankings
    np.random.seed(42)  # Fixed seed for consistency
    
    for metric, metric_name in metrics.items():
        # Randomly assign a ranking (1-30)
        ranking = np.random.randint(1, 31)
        
        # Make them somewhat consistent with the team's win percentage
        if team_stats["WIN_PCT"] > 0.6:  # Good team
            ranking = min(ranking, np.random.randint(1, 15))
        elif team_stats["WIN_PCT"] < 0.4:  # Bad team
            ranking = max(ranking, np.random.randint(15, 31))
        
        # For defensive rating, lower is better, so invert ranking
        if metric == "DRTG":
            value = 31 - ranking
            display_rank = ranking
        else:
            value = ranking
            display_rank = ranking
            
        ranking_data.append({
            "Metric": metric_name,
            "Value": value,
            "Rank": display_rank
        })
    
    # Create DataFrame
    df = pd.DataFrame(ranking_data)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(
        go.Bar(
            y=df["Metric"],
            x=df["Value"],
            orientation='h',
            text=df["Rank"].apply(lambda x: f"#{x}"),
            textposition='auto',
            marker_color=['#4CAF50' if x <= 10 else '#FFC107' if x <= 20 else '#F44336' 
                         for x in df["Rank"]]
        )
    )
    
    # Set layout
    fig.update_layout(
        title=f"{team_name} League Rankings",
        xaxis_title="Rank (1 = Best, 30 = Worst)",
        xaxis=dict(range=[0, 30], dtick=5),
        template="plotly_white",
        height=400
    )
    
    return fig

def create_lineup_chart(lineups_df):
    """Create a bar chart for lineup effectiveness"""
    # Sort by net rating
    lineups_df = lineups_df.sort_values('NET_RTG', ascending=False).head(8)
    
    # Create figure
    fig = go.Figure()
    
    # Add offensive rating bars
    fig.add_trace(
        go.Bar(
            x=lineups_df["LINEUP"],
            y=lineups_df["ORTG"],
            name='Offensive Rating',
            marker_color='#4CAF50'
        )
    )
    
    # Add defensive rating bars
    fig.add_trace(
        go.Bar(
            x=lineups_df["LINEUP"],
            y=lineups_df["DRTG"],
            name='Defensive Rating',
            marker_color='#F44336'
        )
    )
    
    # Add net rating line
    fig.add_trace(
        go.Scatter(
            x=lineups_df["LINEUP"],
            y=lineups_df["NET_RTG"],
            mode='lines+markers',
            name='Net Rating',
            marker_color='#1E88E5',
            line=dict(width=3)
        )
    )
    
    # Set axis labels and title
    fig.update_layout(
        title="Top Lineups by Net Rating",
        xaxis=dict(title='Lineup'),
        yaxis=dict(title='Rating'),
        barmode='group',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=500
    )
    
    # Adjust x-axis for readability
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_player_comparison_chart(players_df):
    """Create a scatter plot comparing players in the team"""
    # Filter active players
    active_players = players_df[players_df["STATUS"] == "Active"]
    
    # Create scatter plot
    fig = px.scatter(
        active_players,
        x="PTS",
        y="AST",
        size="MIN",
        color="POSITION",
        hover_name="PLAYER_NAME",
        hover_data=["REB", "FG_PCT", "FG3_PCT"],
        labels={
            "PTS": "Points Per Game",
            "AST": "Assists Per Game",
            "MIN": "Minutes Per Game",
            "POSITION": "Position"
        },
        title="Player Comparison: Points vs. Assists",
        size_max=25
    )
    
    # Update layout
    fig.update_layout(
        template="plotly_white",
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig

def main():
    st.markdown('<div class="page-title">Team Analysis</div>', unsafe_allow_html=True)
    
    # Database connection status
    db_connected = test_connection()
    
    if not db_connected:
        st.warning("⚠️ Database connection failed. Using sample data for demonstration.", icon="⚠️")
    
    # Team selection sidebar
    st.sidebar.header("Team Selection")
    
    # Get team list (from database or sample)
    teams = get_sample_teams()
    team_options = [t["name"] for t in teams]
    
    # Select team
    selected_team_name = st.sidebar.selectbox("Select Team", team_options)
    selected_team = next((t for t in teams if t["name"] == selected_team_name), None)
    
    if not selected_team:
        st.error("No team selected. Please select a team from the sidebar.")
        return
    
    # Season selection
    current_year = datetime.now().year
    seasons = [f"{year-1}-{str(year)[2:]}" for year in range(current_year-2, current_year+1)]
    
    # Check if season has changed
    if 'previous_season' not in st.session_state:
        st.session_state.previous_season = seasons[-1]  # Default to most recent season
    
    selected_season = st.sidebar.selectbox("Select Season", seasons, index=len(seasons)-1)
    
    # Add a button to clear cache and reload data
    if st.sidebar.button("Refresh Data"):
        # Clear cached data
        get_team_stats.clear()
        get_team_players.clear()
        get_team_lineups.clear()
        st.sidebar.success("Data cache cleared! New data will be loaded.")
    
    # Check if season changed and clear cache automatically
    if st.session_state.previous_season != selected_season:
        get_team_stats.clear()
        get_team_players.clear()
        get_team_lineups.clear()
        st.session_state.previous_season = selected_season
    
    # Load team data
    with st.spinner("Loading team data..."):
        # This would be replaced with database queries in production
        team_stats = get_team_stats(selected_team["id"], selected_season)
        team_players = get_team_players(selected_team["id"], selected_season)
        team_lineups = get_team_lineups(selected_team["id"], selected_season)
    
    # Team header section with logo and basic info
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Team logo (using NBA logo URLs)
        st.image(f"https://cdn.nba.com/logos/nba/{selected_team['id']}/global/L/logo.svg",
                width=150)
    
    with col2:
        # Team info and basic stats
        st.markdown(f"""
        <div class="card">
            <h2>{selected_team_name}</h2>
            <p>{selected_team['conference']}ern Conference | {selected_team['division']} Division</p>
            <p>Season: {selected_season}</p>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <div class="metric-card">
                    <div class="metric-value">{team_stats['WINS']}-{team_stats['LOSSES']}</div>
                    <div class="metric-label">Record</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{team_stats['WIN_PCT']:.3f}</div>
                    <div class="metric-label">Win %</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{team_stats['NET_RTG']:.1f}</div>
                    <div class="metric-label">Net Rating</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{team_stats['PTS_PG']:.1f}</div>
                    <div class="metric-label">PPG</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Team rankings
    st.markdown('<div class="section-title">Team Rankings</div>', unsafe_allow_html=True)
    rankings_chart = create_team_rankings_chart(selected_team_name, team_stats)
    st.plotly_chart(rankings_chart, use_container_width=True)
    
    # Team stats tabs
    st.markdown('<div class="section-title">Team Statistics</div>', unsafe_allow_html=True)
    team_stats_tabs = st.tabs(["Offense", "Defense", "Advanced"])
    
    with team_stats_tabs[0]:
        # Offensive stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['ORTG']:.1f}</div>
                <div class="metric-label">Offensive Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['PTS_PG']:.1f}</div>
                <div class="metric-label">Points Per Game</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['FG_PCT']:.3f}</div>
                <div class="metric-label">FG%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['FG3_PCT']:.3f}</div>
                <div class="metric-label">3PT%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional offensive stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['AST_PG']:.1f}</div>
                <div class="metric-label">Assists Per Game</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['TO_PG']:.1f}</div>
                <div class="metric-label">Turnovers Per Game</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['FT_PCT']:.3f}</div>
                <div class="metric-label">FT%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['AST_RATIO']:.1f}</div>
                <div class="metric-label">Assist Ratio</div>
            </div>
            """, unsafe_allow_html=True)
    
    with team_stats_tabs[1]:
        # Defensive stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['DRTG']:.1f}</div>
                <div class="metric-label">Defensive Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['OPP_PTS_PG']:.1f}</div>
                <div class="metric-label">Opponent PPG</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['STL_PG']:.1f}</div>
                <div class="metric-label">Steals Per Game</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['BLK_PG']:.1f}</div>
                <div class="metric-label">Blocks Per Game</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional defensive stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['REB_PG']:.1f}</div>
                <div class="metric-label">Rebounds Per Game</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['REB_PCT']:.1f}%</div>
                <div class="metric-label">Rebound Percentage</div>
            </div>
            """, unsafe_allow_html=True)
    
    with team_stats_tabs[2]:
        # Advanced stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['TS_PCT']:.3f}</div>
                <div class="metric-label">True Shooting %</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['EFG_PCT']:.3f}</div>
                <div class="metric-label">Effective FG%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['PACE']:.1f}</div>
                <div class="metric-label">Pace</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{team_stats['TO_RATIO']:.1f}</div>
                <div class="metric-label">Turnover Ratio</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Players section
    st.markdown('<div class="section-title">Team Roster</div>', unsafe_allow_html=True)
    
    # Display players table with key stats
    display_columns = ["PLAYER_NAME", "POSITION", "MIN", "PTS", "REB", "AST", 
                       "STL", "BLK", "FG_PCT", "FG3_PCT", "FT_PCT", "STATUS"]
    
    display_df = team_players[display_columns].copy()
    
    # Format percentage columns
    for pct_col in ["FG_PCT", "FG3_PCT", "FT_PCT"]:
        display_df[pct_col] = display_df[pct_col].apply(lambda x: f"{x:.3f}")
    
    # Rename columns for display
    display_df.columns = ["Player", "Pos", "MPG", "PPG", "RPG", "APG", 
                          "SPG", "BPG", "FG%", "3P%", "FT%", "Status"]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Player comparison chart
    player_chart = create_player_comparison_chart(team_players)
    st.plotly_chart(player_chart, use_container_width=True)
    
    # Lineup analysis
    st.markdown('<div class="section-title">Lineup Analysis</div>', unsafe_allow_html=True)
    lineup_chart = create_lineup_chart(team_lineups)
    st.plotly_chart(lineup_chart, use_container_width=True)
    
    # Display top lineups table with detailed stats
    st.markdown('<div class="section-title">Top Lineups Detail</div>', unsafe_allow_html=True)
    
    # Format the lineup dataframe for display
    top_lineups = team_lineups.sort_values('NET_RTG', ascending=False).head(5).copy()
    display_lineups = top_lineups[["LINEUP", "MINUTES", "ORTG", "DRTG", "NET_RTG", "FG_PCT", "FG3_PCT"]].copy()
    
    # Format percentage columns
    for pct_col in ["FG_PCT", "FG3_PCT"]:
        display_lineups[pct_col] = display_lineups[pct_col].apply(lambda x: f"{x:.3f}")
    
    # Format rating columns
    for rtg_col in ["ORTG", "DRTG", "NET_RTG"]:
        display_lineups[rtg_col] = display_lineups[rtg_col].apply(lambda x: f"{x:.1f}")
    
    # Rename columns for display
    display_lineups.columns = ["Lineup", "Minutes", "Off Rtg", "Def Rtg", "Net Rtg", "FG%", "3P%"]
    
    st.dataframe(display_lineups, use_container_width=True, hide_index=True)
    
    # Log page view
    module_logger.info(f"User viewed Team Analysis for {selected_team_name}")

if __name__ == "__main__":
    main() 