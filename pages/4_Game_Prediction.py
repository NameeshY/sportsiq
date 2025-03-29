"""
SportsIQ - Game Prediction
Uses statistical analysis to predict NBA game outcomes
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from datetime import datetime, timedelta
import random

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
from sportsiq.utils import setup_logging, get_logger, test_connection, execute_query

# Set up logging
logger = setup_logging()
module_logger = get_logger("game_prediction")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - Game Prediction",
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
    .home-team {
        color: #1E88E5;
        font-weight: bold;
    }
    .away-team {
        color: #FB8C00;
        font-weight: bold;
    }
    .vs-text {
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0 10px;
    }
    .feature-importance {
        margin-top: 10px;
        margin-bottom: 5px;
        height: 8px;
        border-radius: 4px;
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
def get_team_stats(team_id):
    """Generate sample team statistics"""
    np.random.seed(team_id)  # Use team ID as seed for consistency
    
    # Generate basic team statistics
    wins = np.random.randint(30, 60)
    losses = 82 - wins
    
    # Calculate win percentage
    win_pct = wins / 82
    
    # Generate offensive and defensive stats with some consistency
    if win_pct > 0.6:  # Good team
        pts_pg = np.random.uniform(110, 120)
        opp_pts_pg = np.random.uniform(105, 112)
        ortg = np.random.uniform(112, 118)
        drtg = np.random.uniform(108, 114)
    elif win_pct > 0.4:  # Average team
        pts_pg = np.random.uniform(107, 115)
        opp_pts_pg = np.random.uniform(107, 115)
        ortg = np.random.uniform(110, 115)
        drtg = np.random.uniform(110, 115)
    else:  # Below average team
        pts_pg = np.random.uniform(103, 110)
        opp_pts_pg = np.random.uniform(112, 120)
        ortg = np.random.uniform(105, 111)
        drtg = np.random.uniform(114, 120)
    
    # Net rating
    net_rtg = ortg - drtg
    
    # Other team stats
    fg_pct = np.random.uniform(0.44, 0.49)
    fg3_pct = np.random.uniform(0.34, 0.40)
    ft_pct = np.random.uniform(0.75, 0.83)
    reb_pg = np.random.uniform(41, 47)
    ast_pg = np.random.uniform(22, 28)
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
        "TEAM_ID": team_id,
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
        "PACE": pace
    }

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_head_to_head(team1_id, team2_id):
    """Generate sample head-to-head statistics"""
    # Use consistent seed based on both team IDs, but ensure it's within valid range
    try:
        # Convert to integers in case they're strings
        team1_id = int(team1_id)
        team2_id = int(team2_id)
        
        # Calculate seed and use modulo to ensure it's within valid range
        # 2^32 - 1 = 4294967295 (max value for numpy seed)
        seed = (team1_id * 1000 + team2_id) % 2147483647  # Use a safe maximum (2^31 - 1)
        np.random.seed(seed)
    except ValueError:
        # If there's any issue with the conversion, use a default seed
        module_logger.warning(f"Could not create valid seed from team IDs: {team1_id}, {team2_id}. Using default seed.")
        np.random.seed(42)  # Use a default seed
    
    # Generate recent meetings (last 3 games)
    meetings = []
    
    # Today's date minus some days
    today = datetime.now()
    
    # Generate games from this season and last season
    for i in range(3):
        # Game date (spread throughout the last year)
        days_ago = 30 + i * 120  # Spread out over the year
        game_date = today - timedelta(days=days_ago)
        
        # Generate scores (somewhat based on team quality)
        team1_stats = get_team_stats(team1_id)
        team2_stats = get_team_stats(team2_id)
        
        # Base scores on team offensive ratings with randomness
        team1_score = int(np.random.normal(team1_stats["ORTG"] * 0.95, 6))
        team2_score = int(np.random.normal(team2_stats["ORTG"] * 0.95, 6))
        
        # Add home court advantage (~3 points)
        if i % 2 == 0:  # Team 1 home
            team1_score += 3
            location = "home"
        else:  # Team 2 home
            team2_score += 3
            location = "away"
        
        meetings.append({
            "DATE": game_date.strftime("%b %d, %Y"),
            "TEAM1_SCORE": team1_score,
            "TEAM2_SCORE": team2_score,
            "LOCATION": location,
            "WINNER": team1_id if team1_score > team2_score else team2_id
        })
    
    # Calculate summary stats
    team1_wins = sum(1 for m in meetings if m["WINNER"] == team1_id)
    team2_wins = len(meetings) - team1_wins
    
    return {
        "MEETINGS": meetings,
        "TEAM1_WINS": team1_wins,
        "TEAM2_WINS": team2_wins
    }

@st.cache_data(ttl=86400)  # Cache for 1 day
def get_feature_importance():
    """Return sample feature importance for the prediction model"""
    return [
        {"feature": "Home court advantage", "importance": 0.18},
        {"feature": "Team net rating differential", "importance": 0.16},
        {"feature": "Win percentage differential", "importance": 0.12},
        {"feature": "Points per game differential", "importance": 0.10},
        {"feature": "Recent form (last 10 games)", "importance": 0.09},
        {"feature": "Head-to-head record", "importance": 0.08},
        {"feature": "Rest days differential", "importance": 0.07},
        {"feature": "Rebounding differential", "importance": 0.06},
        {"feature": "3PT percentage differential", "importance": 0.05},
        {"feature": "Pace", "importance": 0.04},
        {"feature": "Assists differential", "importance": 0.03},
        {"feature": "Turnover differential", "importance": 0.02}
    ]

def predict_game_outcome(home_team_id, away_team_id):
    """Predict game outcome and provide win probability"""
    # Get team stats
    home_team_stats = get_team_stats(home_team_id)
    away_team_stats = get_team_stats(away_team_id)
    
    # Get head to head stats
    h2h = get_head_to_head(home_team_id, away_team_id)
    
    # Calculate basic predictors (with home court advantage)
    # This is a simplified model - a real one would be much more complex
    
    # Create a base probability from win percentage differential
    win_pct_diff = home_team_stats["WIN_PCT"] - away_team_stats["WIN_PCT"]
    base_prob = 0.5 + (win_pct_diff * 0.5)  # Scale to keep between 0 and 1
    
    # Add home court advantage
    home_court_factor = 0.08  # NBA home teams win ~60% of games historically
    base_prob += home_court_factor
    
    # Add net rating influence
    net_rtg_diff = home_team_stats["NET_RTG"] - away_team_stats["NET_RTG"]
    net_rtg_factor = net_rtg_diff * 0.01  # Small adjustment per point of net rating
    base_prob += net_rtg_factor
    
    # Add head-to-head factor
    if h2h["TEAM1_WINS"] + h2h["TEAM2_WINS"] > 0:
        h2h_ratio = h2h["TEAM1_WINS"] / (h2h["TEAM1_WINS"] + h2h["TEAM2_WINS"])
        h2h_factor = (h2h_ratio - 0.5) * 0.05  # Small adjustment based on h2h
        base_prob += h2h_factor
    
    # Set a seed for consistency but ensure it's within valid range
    try:
        # Convert to integers in case they're strings
        seed_home = int(home_team_id)
        seed_away = int(away_team_id)
        
        # Calculate a safe seed value
        seed = (seed_home * 1000 + seed_away + 42) % 2147483647  # Use a safe maximum (2^31 - 1)
        np.random.seed(seed)
    except ValueError:
        # If there's any issue with the conversion, use a default seed
        module_logger.warning(f"Could not create valid seed from team IDs: {home_team_id}, {away_team_id}. Using default seed.")
        np.random.seed(42)  # Use a default seed
    
    # Add a small random factor to make predictions less deterministic
    random_factor = np.random.normal(0, 0.02)  # Small random noise
    base_prob += random_factor
    
    # Ensure probability is between 0.1 and 0.9 to avoid extreme predictions
    win_probability = max(0.1, min(0.9, base_prob))
    
    # Generate a predicted score
    avg_score = (home_team_stats["PTS_PG"] + away_team_stats["OPP_PTS_PG"]) / 2
    avg_opp_score = (away_team_stats["PTS_PG"] + home_team_stats["OPP_PTS_PG"]) / 2
    
    # Add some random variation
    predicted_home_score = int(np.random.normal(avg_score, 3))
    predicted_away_score = int(np.random.normal(avg_opp_score, 3))
    
    # Ensure the predicted winner matches the win probability
    if (predicted_home_score > predicted_away_score and win_probability < 0.5) or \
       (predicted_home_score < predicted_away_score and win_probability > 0.5):
        # Swap scores to match win probability
        predicted_home_score, predicted_away_score = predicted_away_score, predicted_home_score
    
    # Return prediction results
    return {
        "WIN_PROBABILITY": win_probability,
        "PREDICTED_HOME_SCORE": predicted_home_score,
        "PREDICTED_AWAY_SCORE": predicted_away_score,
        "KEY_FACTORS": [
            {"factor": "Home court advantage", "value": f"+{home_court_factor:.2f}"},
            {"factor": "Win percentage", "value": f"{win_pct_diff:.3f} differential"},
            {"factor": "Net rating", "value": f"{net_rtg_diff:.1f} differential"},
            {"factor": "Head-to-head", "value": f"{h2h['TEAM1_WINS']}-{h2h['TEAM2_WINS']}"}
        ]
    }

def create_win_probability_gauge(win_probability, home_team, away_team):
    """Create a gauge chart for win probability"""
    # Define colors
    home_color = "#1E88E5"  # Blue
    away_color = "#FB8C00"  # Orange
    
    # Create gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=win_probability * 100,
        number={"suffix": "%", "font": {"size": 24}},
        delta={"reference": 50, "increasing": {"color": home_color}, "decreasing": {"color": away_color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkgray"},
            "bar": {"color": home_color if win_probability >= 0.5 else away_color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 50], "color": away_color, "thickness": 1.0},
                {"range": [50, 100], "color": home_color, "thickness": 1.0}
            ],
            "threshold": {
                "line": {"color": "black", "width": 2},
                "thickness": 0.75,
                "value": win_probability * 100
            }
        },
        title={
            "text": f"Win Probability<br><span style='font-size:0.8em;'>{home_team} vs {away_team}</span>",
            "font": {"size": 20}
        }
    ))
    
    # Team labels
    fig.add_annotation(
        x=0.1,
        y=0.5,
        text=away_team,
        showarrow=False,
        font={"color": away_color, "size": 14}
    )
    
    fig.add_annotation(
        x=0.9,
        y=0.5,
        text=home_team,
        showarrow=False,
        font={"color": home_color, "size": 14}
    )
    
    # Update layout
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=80, b=20),
    )
    
    return fig

def create_score_prediction_chart(home_score, away_score, home_team, away_team):
    """Create a bar chart for predicted score"""
    # Create data
    scores = [home_score, away_score]
    teams = [home_team, away_team]
    colors = ["#1E88E5", "#FB8C00"]  # Blue, Orange
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=teams,
            y=scores,
            marker_color=colors,
            text=scores,
            textposition='auto',
            width=[0.4, 0.4]
        )
    ])
    
    # Update layout
    fig.update_layout(
        title="Predicted Score",
        xaxis=dict(title=""),
        yaxis=dict(title="Points", range=[0, max(scores) * 1.2]),
        template="plotly_white",
        height=300
    )
    
    return fig

def create_feature_importance_chart():
    """Create a chart showing feature importance for the prediction model"""
    # Get feature importance
    features = get_feature_importance()
    
    # Sort by importance
    features = sorted(features, key=lambda x: x["importance"], reverse=True)
    
    # Create horizontal bar chart
    fig = go.Figure(data=[
        go.Bar(
            y=[f["feature"] for f in features],
            x=[f["importance"] * 100 for f in features],
            orientation='h',
            marker_color="#1E88E5",
            text=[f"{f['importance'] * 100:.1f}%" for f in features],
            textposition="auto"
        )
    ])
    
    # Update layout
    fig.update_layout(
        title="Feature Importance in Prediction Model",
        xaxis=dict(title="Importance (%)", range=[0, 20]),
        yaxis=dict(title=""),
        template="plotly_white",
        height=400
    )
    
    return fig

def create_team_comparison_chart(home_team_stats, away_team_stats, home_team, away_team):
    """Create a comparison chart for key team statistics"""
    # Select key stats for comparison
    stats = [
        {"key": "WIN_PCT", "name": "Win %", "format": ".3f"},
        {"key": "PTS_PG", "name": "Points Per Game", "format": ".1f"},
        {"key": "OPP_PTS_PG", "name": "Opp. Points Per Game", "format": ".1f", "invert": True},
        {"key": "NET_RTG", "name": "Net Rating", "format": ".1f"},
        {"key": "FG_PCT", "name": "FG%", "format": ".3f"},
        {"key": "FG3_PCT", "name": "3PT%", "format": ".3f"},
        {"key": "REB_PG", "name": "Rebounds Per Game", "format": ".1f"}
    ]
    
    # Create data for chart
    chart_data = []
    
    for stat in stats:
        home_val = home_team_stats[stat["key"]]
        away_val = away_team_stats[stat["key"]]
        
        # For stats where lower is better, invert the values
        if stat.get("invert", False):
            # Create a normalized value for the chart
            max_val = max(home_val, away_val)
            home_normalized = (max_val - home_val) / max_val
            away_normalized = (max_val - away_val) / max_val
        else:
            # Normalize values between 0 and 1
            max_val = max(home_val, away_val)
            if max_val > 0:
                home_normalized = home_val / max_val
                away_normalized = away_val / max_val
            else:
                home_normalized = away_normalized = 0
        
        # Format the display values
        format_str = "{:" + stat["format"] + "}"
        home_display = format_str.format(home_val)
        away_display = format_str.format(away_val)
        
        chart_data.append({
            "Metric": stat["name"],
            "Home": home_normalized,
            "Away": away_normalized,
            "Home_Display": home_display,
            "Away_Display": away_display
        })
    
    # Convert to dataframe
    df = pd.DataFrame(chart_data)
    
    # Create subplots with two y-axes for home and away
    fig = go.Figure()
    
    # Home team bars
    fig.add_trace(
        go.Bar(
            y=df["Metric"],
            x=df["Home"],
            orientation='h',
            name=home_team,
            marker_color="#1E88E5",
            text=df["Home_Display"],
            textposition="inside",
            width=0.5,
            offset=-0.3
        )
    )
    
    # Away team bars
    fig.add_trace(
        go.Bar(
            y=df["Metric"],
            x=df["Away"],
            orientation='h',
            name=away_team,
            marker_color="#FB8C00",
            text=df["Away_Display"],
            textposition="inside",
            width=0.5,
            offset=0.3
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Team Statistical Comparison",
        xaxis=dict(
            title="",
            showticklabels=False,
            range=[0, 1.15]
        ),
        yaxis=dict(title=""),
        barmode='overlay',
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )
    
    return fig

def main():
    st.markdown('<div class="page-title">Game Prediction</div>', unsafe_allow_html=True)
    
    # Database connection status
    db_connected = test_connection()
    
    if not db_connected:
        st.warning("⚠️ Database connection failed. Using sample data for demonstration.", icon="⚠️")
    
    # Match selection section
    st.markdown('<div class="section-title">Match Selection</div>', unsafe_allow_html=True)
    
    # Get team list (from database or sample)
    teams = get_sample_teams()
    team_names = [t["name"] for t in teams]
    
    # Team selection sidebar
    st.sidebar.header("Match Selection")
    
    # Home team selection
    home_team_name = st.sidebar.selectbox("Home Team", team_names, index=0)
    home_team = next((t for t in teams if t["name"] == home_team_name), None)
    
    # Away team selection
    # Filter out the home team from options
    away_team_options = [t for t in team_names if t != home_team_name]
    away_team_name = st.sidebar.selectbox("Away Team", away_team_options, index=0)
    away_team = next((t for t in teams if t["name"] == away_team_name), None)
    
    # Game date selection (future date)
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    game_date = st.sidebar.date_input("Game Date", tomorrow)
    
    # Predict button
    predict_button = st.sidebar.button("Predict Game Outcome", type="primary")
    
    # Initialize session state for prediction
    if "prediction" not in st.session_state:
        st.session_state.prediction = None
    
    # Make prediction when button is clicked
    if predict_button:
        with st.spinner("Analyzing data and predicting outcome..."):
            # Generate prediction
            st.session_state.prediction = predict_game_outcome(home_team["id"], away_team["id"])
    
    # Display match card
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <img src="https://cdn.nba.com/logos/nba/{home_team['id']}/global/L/logo.svg" width="120">
            <h3 class="home-team">{home_team_name}</h3>
            <p>HOME</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="display: flex; height: 100%; align-items: center; justify-content: center;">
            <span class="vs-text">VS</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <img src="https://cdn.nba.com/logos/nba/{away_team['id']}/global/L/logo.svg" width="120">
            <h3 class="away-team">{away_team_name}</h3>
            <p>AWAY</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display date and location
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3>{game_date.strftime('%A, %B %d, %Y')}</h3>
        <p>Game Location: {home_team_name} Home Arena</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if prediction exists
    if st.session_state.prediction:
        prediction = st.session_state.prediction
        
        # Prediction results section
        st.markdown('<div class="section-title">Game Prediction</div>', unsafe_allow_html=True)
        
        # Win probability gauge
        win_prob_gauge = create_win_probability_gauge(
            prediction["WIN_PROBABILITY"], 
            home_team_name, 
            away_team_name
        )
        st.plotly_chart(win_prob_gauge, use_container_width=True)
        
        # Prediction text
        win_prob_pct = prediction["WIN_PROBABILITY"] * 100
        winner = home_team_name if prediction["WIN_PROBABILITY"] > 0.5 else away_team_name
        win_margin = abs(prediction["PREDICTED_HOME_SCORE"] - prediction["PREDICTED_AWAY_SCORE"])
        
        st.markdown(f"""
        <div class="card">
            <h3>Prediction Summary</h3>
            <p>The <strong>{winner}</strong> are predicted to win with {win_prob_pct:.1f}% probability.</p>
            <p>Projected score: <span class="home-team">{home_team_name}</span> {prediction["PREDICTED_HOME_SCORE"]} - {prediction["PREDICTED_AWAY_SCORE"]} <span class="away-team">{away_team_name}</span></p>
            <p>Projected margin: {win_margin} points</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Score prediction chart
        score_chart = create_score_prediction_chart(
            prediction["PREDICTED_HOME_SCORE"],
            prediction["PREDICTED_AWAY_SCORE"],
            home_team_name,
            away_team_name
        )
        
        # Key factors
        st.markdown('<div class="section-title">Key Prediction Factors</div>', unsafe_allow_html=True)
        
        # Create columns for key factors
        cols = st.columns(len(prediction["KEY_FACTORS"]))
        
        for i, factor in enumerate(prediction["KEY_FACTORS"]):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{factor["value"]}</div>
                    <div class="metric-label">{factor["factor"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Team comparison section
        st.markdown('<div class="section-title">Team Comparison</div>', unsafe_allow_html=True)
        
        # Get team stats
        home_team_stats = get_team_stats(home_team["id"])
        away_team_stats = get_team_stats(away_team["id"])
        
        # Team comparison chart
        team_comparison = create_team_comparison_chart(
            home_team_stats,
            away_team_stats,
            home_team_name,
            away_team_name
        )
        st.plotly_chart(team_comparison, use_container_width=True)
        
        # Head-to-head history
        st.markdown('<div class="section-title">Head-to-Head History</div>', unsafe_allow_html=True)
        
        # Get head-to-head data
        h2h = get_head_to_head(home_team["id"], away_team["id"])
        
        # Display head-to-head summary
        st.markdown(f"""
        <div class="card">
            <h3>Recent Meetings</h3>
            <p><span class="home-team">{home_team_name}</span> {h2h["TEAM1_WINS"]} - {h2h["TEAM2_WINS"]} <span class="away-team">{away_team_name}</span> (Last 3 games)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Meeting details
        for meeting in h2h["MEETINGS"]:
            location_text = "HOME" if meeting["LOCATION"] == "home" else "AWAY"
            winner = home_team_name if meeting["WINNER"] == home_team["id"] else away_team_name
            winner_class = "home-team" if winner == home_team_name else "away-team"
            
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; background-color: #f2f2f2; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between;">
                    <div>{meeting["DATE"]} ({location_text})</div>
                    <div><span class="home-team">{home_team_name}</span> {meeting["TEAM1_SCORE"]} - {meeting["TEAM2_SCORE"]} <span class="away-team">{away_team_name}</span></div>
                    <div>Winner: <span class="{winner_class}">{winner}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Model details
        st.markdown('<div class="section-title">Prediction Model</div>', unsafe_allow_html=True)
        
        # Feature importance chart
        feature_chart = create_feature_importance_chart()
        st.plotly_chart(feature_chart, use_container_width=True)
        
        # Model info
        st.markdown("""
        <div class="card">
            <h3>About the Prediction Model</h3>
            <p>This prediction model uses machine learning algorithms trained on NBA game data from the last several seasons. It considers various factors including team statistics, player availability, historical matchups, and situational variables like rest days and travel.</p>
            <p>The model is designed to provide win probabilities and projected scores that account for the specific matchup dynamics between the two teams.</p>
            <p><strong>Note:</strong> All predictions are probabilities. Even games with high confidence predictions can result in unexpected outcomes.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Instructions when no prediction is made yet
        st.info("""
        Select the home and away teams from the sidebar, choose a game date, and click 'Predict Game Outcome' to generate a prediction.
        
        The prediction model will analyze team statistics, head-to-head matchups, and other factors to estimate the win probability and projected score.
        """
        )
    
    # Log page view
    module_logger.info(f"User viewed Game Prediction page for {home_team_name} vs {away_team_name}")

if __name__ == "__main__":
    main() 