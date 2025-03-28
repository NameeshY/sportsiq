"""
SportsIQ - Injury Risk Analysis
Provides insights on player workload and injury risk assessment
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

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
from sportsiq.utils import setup_logging, get_logger, test_connection, execute_query

# Set up logging
logger = setup_logging()
module_logger = get_logger("injury_risk")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - Injury Risk Analysis",
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
    .risk-high {
        color: #D32F2F;
        font-weight: bold;
    }
    .risk-medium {
        color: #FFA000;
        font-weight: bold;
    }
    .risk-low {
        color: #388E3C;
        font-weight: bold;
    }
    .card {
        border-radius: 5px;
        padding: 1.5rem;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .indicator-card {
        text-align: center;
        padding: 1rem;
        border-radius: 5px;
        background-color: #f5f5f5;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .indicator-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .indicator-label {
        font-size: 0.9rem;
        color: #616161;
    }
    .insight-box {
        padding: 1rem;
        background-color: #e3f2fd;
        border-left: 4px solid #1E88E5;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sample data functions (would be replaced by real database queries)
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_sample_players():
    """Return a sample list of NBA players"""
    return [
        {"id": 2544, "name": "LeBron James", "team": "Los Angeles Lakers", "position": "F", "age": 38},
        {"id": 201939, "name": "Stephen Curry", "team": "Golden State Warriors", "position": "G", "age": 35},
        {"id": 203954, "name": "Joel Embiid", "team": "Philadelphia 76ers", "position": "C", "age": 29},
        {"id": 203507, "name": "Giannis Antetokounmpo", "team": "Milwaukee Bucks", "position": "F", "age": 28},
        {"id": 201142, "name": "Kevin Durant", "team": "Phoenix Suns", "position": "F", "age": 34},
        {"id": 1629027, "name": "Luka Doncic", "team": "Dallas Mavericks", "position": "G-F", "age": 24},
        {"id": 1628369, "name": "Jayson Tatum", "team": "Boston Celtics", "position": "F", "age": 25},
        {"id": 201566, "name": "Nikola Jokic", "team": "Denver Nuggets", "position": "C", "age": 28},
        {"id": 1628983, "name": "Shai Gilgeous-Alexander", "team": "OKC Thunder", "position": "G", "age": 25},
        {"id": 1627783, "name": "Donovan Mitchell", "team": "Cleveland Cavaliers", "position": "G", "age": 27}
    ]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_player_fatigue_metrics(player_id):
    """Generate sample fatigue metrics for a player"""
    np.random.seed(player_id)  # Use player ID as seed for consistency
    
    # Create dates for the last 30 games
    end_date = datetime.now() - timedelta(days=2)
    game_dates = [end_date - timedelta(days=i*2) for i in range(30)]
    game_dates.reverse()  # Oldest to newest
    
    # Base values
    base_minutes = np.random.randint(28, 35)
    base_usage = np.random.randint(24, 32)
    
    # Generate metrics
    metrics = []
    
    # Initialize variables for calculating cumulative metrics
    last_game_date = None
    
    for i, game_date in enumerate(game_dates):
        # Minutes played with some randomness
        minutes = max(20, min(40, base_minutes + np.random.randint(-6, 7)))
        
        # Days of rest since last game
        days_rest = (game_date - last_game_date).days if last_game_date else 3
        last_game_date = game_date
        
        # Count games in last 7 days
        games_last_7_days = sum(1 for d in game_dates[max(0, i-7):i+1] 
                               if (game_date - d).days <= 7)
        
        # Calculate minutes in last 7 days
        minutes_last_7_days = sum(np.random.randint(base_minutes-5, base_minutes+6) 
                                 for _ in range(games_last_7_days))
        
        # Usage rate (with trend - slightly increasing over time to simulate fatigue)
        usage_pct = base_usage + np.random.randint(-3, 4) + (i // 10)
        usage_pct = min(45, max(15, usage_pct))  # Keep within reasonable bounds
        
        # Create 5-game rolling average for minutes
        if i >= 4:
            min_rolling_avg_5 = sum(metrics[j]['MINUTES'] for j in range(i-4, i)) / 4
        else:
            min_rolling_avg_5 = base_minutes
        
        # Calculate fatigue score (more complex in reality)
        # Formula: weighted sum of factors that contribute to fatigue
        fatigue_score = (
            (minutes / 48) * 35 +  # Minutes contribution (max 35 points)
            (min(10, 10 - days_rest*2)) +  # Recent rest contribution (max 10 points)
            (games_last_7_days / 5) * 20 +  # Games density contribution (max 20 points)
            (usage_pct / 40) * 25 +  # Usage rate contribution (max 25 points)
            (minutes_last_7_days / 240) * 10  # 7-day workload contribution (max 10 points)
        )
        
        # Add injury risk probability (logistic function of fatigue score)
        risk_probability = 1 / (1 + np.exp(-0.05 * (fatigue_score - 50)))
        
        # Create opponent from list of teams
        teams = ["BOS", "MIA", "PHI", "TOR", "CHI", "CLE", "MIL", "NYK", "ATL", "CHA", 
                "LAL", "GSW", "PHX", "LAC", "DEN", "MEM", "DAL", "POR", "UTA", "SAC"]
        opponent = teams[i % len(teams)]
        
        metrics.append({
            "GAME_DATE": game_date,
            "MATCHUP": f"vs. {opponent}",
            "MINUTES": minutes,
            "DAYS_REST": days_rest,
            "GAMES_LAST_7_DAYS": games_last_7_days,
            "MINUTES_LAST_7_DAYS": minutes_last_7_days,
            "USAGE_PCT": usage_pct,
            "MIN_ROLLING_AVG_5": min_rolling_avg_5,
            "FATIGUE_SCORE": fatigue_score,
            "RISK_PROBABILITY": risk_probability
        })
    
    return pd.DataFrame(metrics)

def create_fatigue_trend_chart(fatigue_metrics, player_name):
    """Create a line chart showing fatigue trends over time"""
    # Sort by date
    fatigue_metrics = fatigue_metrics.sort_values('GAME_DATE')
    
    # Create figure
    fig = go.Figure()
    
    # Add fatigue score line
    fig.add_trace(
        go.Scatter(
            x=fatigue_metrics['GAME_DATE'],
            y=fatigue_metrics['FATIGUE_SCORE'],
            mode='lines+markers',
            name='Fatigue Score',
            line=dict(color='#E53935', width=3),
            marker=dict(size=8)
        )
    )
    
    # Add risk zones
    fig.add_shape(
        type="rect",
        x0=fatigue_metrics['GAME_DATE'].min(),
        x1=fatigue_metrics['GAME_DATE'].max(),
        y0=70,
        y1=100,
        fillcolor="rgba(231, 76, 60, 0.2)",
        line_width=0,
        layer="below"
    )
    
    fig.add_shape(
        type="rect",
        x0=fatigue_metrics['GAME_DATE'].min(),
        x1=fatigue_metrics['GAME_DATE'].max(),
        y0=40,
        y1=70,
        fillcolor="rgba(241, 196, 15, 0.2)",
        line_width=0,
        layer="below"
    )
    
    fig.add_shape(
        type="rect",
        x0=fatigue_metrics['GAME_DATE'].min(),
        x1=fatigue_metrics['GAME_DATE'].max(),
        y0=0,
        y1=40,
        fillcolor="rgba(46, 204, 113, 0.2)",
        line_width=0,
        layer="below"
    )
    
    # Add labels for risk zones
    fig.add_annotation(
        x=fatigue_metrics['GAME_DATE'].max(),
        y=85,
        text="High Risk",
        showarrow=False,
        font=dict(color="rgba(231, 76, 60, 1)", size=12)
    )
    
    fig.add_annotation(
        x=fatigue_metrics['GAME_DATE'].max(),
        y=55,
        text="Moderate Risk",
        showarrow=False,
        font=dict(color="rgba(241, 196, 15, 1)", size=12)
    )
    
    fig.add_annotation(
        x=fatigue_metrics['GAME_DATE'].max(),
        y=20,
        text="Low Risk",
        showarrow=False,
        font=dict(color="rgba(46, 204, 113, 1)", size=12)
    )
    
    # Set layout
    fig.update_layout(
        title=f"{player_name} - Fatigue Score Trend",
        xaxis_title="Game Date",
        yaxis_title="Fatigue Score",
        yaxis=dict(range=[0, 100]),
        template="plotly_white",
        hovermode="x unified"
    )
    
    return fig

def create_workload_chart(fatigue_metrics, player_name):
    """Create a chart showing workload factors over time"""
    # Sort by date
    fatigue_metrics = fatigue_metrics.sort_values('GAME_DATE')
    
    # Create subplots with 3 rows
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            "Minutes Played", 
            "Games in Last 7 Days",
            "Usage Percentage"
        ),
        shared_xaxes=True,
        vertical_spacing=0.1
    )
    
    # Add minutes trend
    fig.add_trace(
        go.Scatter(
            x=fatigue_metrics['GAME_DATE'],
            y=fatigue_metrics['MINUTES'],
            mode='lines+markers',
            name='Minutes',
            line=dict(color='#1E88E5')
        ),
        row=1, col=1
    )
    
    # Add 5-game rolling average for minutes
    fig.add_trace(
        go.Scatter(
            x=fatigue_metrics['GAME_DATE'],
            y=fatigue_metrics['MIN_ROLLING_AVG_5'],
            mode='lines',
            name='5-Game Avg Minutes',
            line=dict(color='#5E35B1', dash='dash')
        ),
        row=1, col=1
    )
    
    # Add games in last 7 days
    fig.add_trace(
        go.Scatter(
            x=fatigue_metrics['GAME_DATE'],
            y=fatigue_metrics['GAMES_LAST_7_DAYS'],
            mode='lines+markers',
            name='Games (7 Days)',
            line=dict(color='#43A047')
        ),
        row=2, col=1
    )
    
    # Add usage percentage
    fig.add_trace(
        go.Scatter(
            x=fatigue_metrics['GAME_DATE'],
            y=fatigue_metrics['USAGE_PCT'],
            mode='lines+markers',
            name='Usage %',
            line=dict(color='#FB8C00')
        ),
        row=3, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        title=f"{player_name} - Workload Factors",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified"
    )
    
    # Update y-axes ranges
    fig.update_yaxes(title_text="Minutes", range=[15, 45], row=1, col=1)
    fig.update_yaxes(title_text="Games", range=[0, 6], dtick=1, row=2, col=1)
    fig.update_yaxes(title_text="Usage %", range=[15, 45], row=3, col=1)
    
    return fig

def create_risk_gauge(risk_probability, title="Current Injury Risk"):
    """Create a gauge chart to visualize injury risk"""
    # Determine color based on risk level
    if risk_probability < 0.3:
        color = "#4CAF50"  # Green for low risk
        risk_level = "Low"
    elif risk_probability < 0.6:
        color = "#FFC107"  # Amber for moderate risk
        risk_level = "Moderate"
    else:
        color = "#F44336"  # Red for high risk
        risk_level = "High"
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_probability * 100,  # Convert to percentage
        title={"text": title, "font": {"size": 16}},
        number={"suffix": "%", "font": {"color": color, "size": 20}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkgray"},
            "bar": {"color": color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 30], "color": "rgba(76, 175, 80, 0.3)"},  # Green zone
                {"range": [30, 60], "color": "rgba(255, 193, 7, 0.3)"},  # Amber zone
                {"range": [60, 100], "color": "rgba(244, 67, 54, 0.3)"}  # Red zone
            ],
            "threshold": {
                "line": {"color": "black", "width": 3},
                "thickness": 0.75,
                "value": risk_probability * 100
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig, risk_level

def get_risk_insights(fatigue_metrics, player_name, player_age):
    """Generate insights based on fatigue metrics and risk assessment"""
    insights = []
    
    # Get latest metrics
    latest_metrics = fatigue_metrics.sort_values('GAME_DATE', ascending=False).iloc[0]
    recent_metrics = fatigue_metrics.sort_values('GAME_DATE', ascending=False).head(5)
    
    # Insight on current risk level
    risk_prob = latest_metrics['RISK_PROBABILITY']
    if risk_prob > 0.6:
        insights.append(f"⚠️ {player_name} currently has a <span class='risk-high'>HIGH</span> injury risk probability of {risk_prob:.1%}.")
    elif risk_prob > 0.3:
        insights.append(f"⚠️ {player_name} currently has a <span class='risk-medium'>MODERATE</span> injury risk probability of {risk_prob:.1%}.")
    else:
        insights.append(f"✅ {player_name} currently has a <span class='risk-low'>LOW</span> injury risk probability of {risk_prob:.1%}.")
    
    # Insight on minutes load
    recent_avg_minutes = recent_metrics['MINUTES'].mean()
    if recent_avg_minutes > 36:
        insights.append(f"⏱️ {player_name} is playing {recent_avg_minutes:.1f} minutes per game in the last 5 games, which is substantially above the recommended limit.")
    elif recent_avg_minutes > 32:
        insights.append(f"⏱️ {player_name} is playing {recent_avg_minutes:.1f} minutes per game in the last 5 games, which is on the higher end but manageable.")
    
    # Insight on game density
    if latest_metrics['GAMES_LAST_7_DAYS'] >= 4:
        insights.append(f"📅 {player_name} has played {latest_metrics['GAMES_LAST_7_DAYS']} games in the last 7 days, indicating high schedule density and limited recovery time.")
    
    # Insight on rest
    if latest_metrics['DAYS_REST'] < 2:
        insights.append(f"😴 {player_name} has had only {latest_metrics['DAYS_REST']} day(s) of rest before the most recent game. Insufficient rest increases injury risk.")
    
    # Insight on usage rate
    if latest_metrics['USAGE_PCT'] > 30:
        insights.append(f"📊 {player_name}'s usage rate of {latest_metrics['USAGE_PCT']:.1f}% is very high, putting additional strain on their body.")
    
    # Insight based on age
    if player_age > 32:
        insights.append(f"👴 At {player_age} years old, {player_name} has increased recovery needs. The current workload should be carefully managed.")
    
    # Insight on trend
    recent_trend = fatigue_metrics.sort_values('GAME_DATE', ascending=True).tail(10)['FATIGUE_SCORE']
    
    if recent_trend.iloc[-1] > recent_trend.iloc[0] * 1.2:
        insights.append(f"📈 {player_name}'s fatigue score has increased by {((recent_trend.iloc[-1] / recent_trend.iloc[0]) - 1) * 100:.1f}% over the last 10 games, suggesting accumulating fatigue.")
    
    return insights

def main():
    st.markdown('<div class="page-title">Injury Risk Analysis</div>', unsafe_allow_html=True)
    
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
    
    # Introduction to the injury risk analysis
    st.markdown("""
    <div class="card">
        <h3>About Injury Risk Analysis</h3>
        <p>This analysis evaluates multiple factors that contribute to player fatigue and potential injury risk, including:</p>
        <ul>
            <li><strong>Minutes Played</strong>: Total minutes and recent averages</li>
            <li><strong>Game Density</strong>: Number of games in short time periods</li>
            <li><strong>Rest</strong>: Days between games</li>
            <li><strong>Usage Rate</strong>: Player's involvement in team plays</li>
            <li><strong>Age</strong>: Recovery needs based on player age</li>
        </ul>
        <p>The model calculates a <strong>Fatigue Score</strong> and <strong>Risk Probability</strong> to help teams manage player workload.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load player data
    with st.spinner("Analyzing injury risk..."):
        # This would be replaced with database queries in production
        fatigue_metrics = get_player_fatigue_metrics(selected_player["id"])
    
    # Current risk overview
    st.markdown('<div class="section-title">Current Risk Assessment</div>', unsafe_allow_html=True)
    
    # Get latest metrics
    latest_metrics = fatigue_metrics.sort_values('GAME_DATE', ascending=False).iloc[0]
    
    # Create columns for risk indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Risk gauge
        fig, risk_level = create_risk_gauge(latest_metrics['RISK_PROBABILITY'], "Injury Risk")
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk level text with appropriate color
        risk_color_class = f"risk-{risk_level.lower()}"
        st.markdown(f"<div style='text-align: center;'>Risk Level: <span class='{risk_color_class}'>{risk_level}</span></div>", unsafe_allow_html=True)
    
    with col2:
        # Fatigue score
        st.markdown("""
        <div class="indicator-card">
            <div class="indicator-value" style="color: #E53935;">{:.1f}</div>
            <div class="indicator-label">Fatigue Score</div>
        </div>
        """.format(latest_metrics['FATIGUE_SCORE']), unsafe_allow_html=True)
        
        # Recent workload
        st.markdown("""
        <div class="indicator-card" style="margin-top: 1rem;">
            <div class="indicator-value" style="color: #FB8C00;">{}</div>
            <div class="indicator-label">Minutes Last Game</div>
        </div>
        """.format(latest_metrics['MINUTES']), unsafe_allow_html=True)
    
    with col3:
        # Game density
        st.markdown("""
        <div class="indicator-card">
            <div class="indicator-value" style="color: #43A047;">{}</div>
            <div class="indicator-label">Games in Last 7 Days</div>
        </div>
        """.format(latest_metrics['GAMES_LAST_7_DAYS']), unsafe_allow_html=True)
        
        # Rest days
        st.markdown("""
        <div class="indicator-card" style="margin-top: 1rem;">
            <div class="indicator-value" style="color: #1E88E5;">{}</div>
            <div class="indicator-label">Days Rest Before Last Game</div>
        </div>
        """.format(latest_metrics['DAYS_REST']), unsafe_allow_html=True)
    
    with col4:
        # Player info
        st.markdown("""
        <div class="card">
            <h4>{}</h4>
            <p>{} | {}</p>
            <p>Age: {}</p>
            <p>Last Game: {}</p>
        </div>
        """.format(
            selected_player['name'],
            selected_player['team'],
            selected_player['position'],
            selected_player['age'],
            latest_metrics['GAME_DATE'].strftime('%b %d, %Y')
        ), unsafe_allow_html=True)
    
    # Insights
    st.markdown('<div class="section-title">Risk Insights</div>', unsafe_allow_html=True)
    
    insights = get_risk_insights(fatigue_metrics, selected_player_name, selected_player['age'])
    
    for insight in insights:
        st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)
    
    # Fatigue trend chart
    st.markdown('<div class="section-title">Fatigue Trend Analysis</div>', unsafe_allow_html=True)
    
    # Create fatigue trend chart
    fatigue_chart = create_fatigue_trend_chart(fatigue_metrics, selected_player_name)
    st.plotly_chart(fatigue_chart, use_container_width=True)
    
    # Workload analysis
    st.markdown('<div class="section-title">Workload Analysis</div>', unsafe_allow_html=True)
    
    # Create workload chart
    workload_chart = create_workload_chart(fatigue_metrics, selected_player_name)
    st.plotly_chart(workload_chart, use_container_width=True)
    
    # Risk factors table
    st.markdown('<div class="section-title">Detailed Risk Factors</div>', unsafe_allow_html=True)
    
    # Filter columns and format date column
    display_cols = ['GAME_DATE', 'MATCHUP', 'MINUTES', 'DAYS_REST', 'GAMES_LAST_7_DAYS', 
                    'USAGE_PCT', 'FATIGUE_SCORE', 'RISK_PROBABILITY']
    
    display_df = fatigue_metrics[display_cols].sort_values('GAME_DATE', ascending=False).copy()
    display_df['GAME_DATE'] = display_df['GAME_DATE'].dt.strftime('%b %d, %Y')
    display_df['RISK_PROBABILITY'] = display_df['RISK_PROBABILITY'].apply(lambda x: f"{x:.1%}")
    display_df['FATIGUE_SCORE'] = display_df['FATIGUE_SCORE'].apply(lambda x: f"{x:.1f}")
    display_df['USAGE_PCT'] = display_df['USAGE_PCT'].apply(lambda x: f"{x:.1f}%")
    
    # Rename columns for display
    display_df.columns = ['Game Date', 'Matchup', 'Minutes', 'Days Rest', 'Games in 7 Days', 
                         'Usage %', 'Fatigue Score', 'Risk Probability']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Recommendations based on current risk level
    st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)
    
    if latest_metrics['RISK_PROBABILITY'] > 0.6:
        st.markdown("""
        <div class="card" style="border-left: 4px solid #F44336;">
            <h4>High Risk - Action Required</h4>
            <ul>
                <li>Consider <strong>resting the player</strong> for the next game</li>
                <li>If rest is not possible, <strong>limit minutes</strong> to 20-25</li>
                <li>Implement <strong>additional recovery protocols</strong> (massage, cold therapy)</li>
                <li>Reduce usage rate by <strong>redistributing offensive load</strong></li>
                <li>Conduct daily <strong>physical assessments</strong> to monitor recovery</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif latest_metrics['RISK_PROBABILITY'] > 0.3:
        st.markdown("""
        <div class="card" style="border-left: 4px solid #FFC107;">
            <h4>Moderate Risk - Caution Advised</h4>
            <ul>
                <li><strong>Limit minutes</strong> to 25-30 in the next game</li>
                <li>Schedule <strong>additional rest days</strong> between games if possible</li>
                <li>Increase <strong>recovery focus</strong> with additional treatment sessions</li>
                <li>Consider <strong>reduced role</strong> in high-intensity situations</li>
                <li>Monitor <strong>movement patterns</strong> for signs of compensation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="border-left: 4px solid #4CAF50;">
            <h4>Low Risk - Normal Management</h4>
            <ul>
                <li>Continue <strong>standard minutes</strong> and role</li>
                <li>Maintain <strong>regular recovery protocols</strong></li>
                <li>Implement <strong>preventative measures</strong> to avoid risk increase</li>
                <li>Continue <strong>normal monitoring</strong> of physical readiness</li>
                <li>Be attentive to any <strong>minor discomforts</strong> that may develop</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Log page view
    module_logger.info(f"User viewed Injury Risk Analysis for {selected_player_name}")

if __name__ == "__main__":
    main() 