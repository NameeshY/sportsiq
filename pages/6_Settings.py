"""
SportsIQ - Settings Page
Allows users to configure the application settings and preferences
"""
import streamlit as st
import pandas as pd
import os
import sys
import json
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
from sportsiq.utils import setup_logging, get_logger

# Set up logging
logger = setup_logging()
module_logger = get_logger("settings")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - Settings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the settings file path
SETTINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "user_settings.json")

# Ensure the settings directory exists
if not os.path.exists(SETTINGS_DIR):
    os.makedirs(SETTINGS_DIR)

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
    .settings-card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .settings-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .settings-description {
        font-size: 0.9rem;
        color: #616161;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    .status-success {
        background-color: #E8F5E9;
        color: #2E7D32;
    }
    .status-warning {
        background-color: #FFF8E1;
        color: #F57F17;
    }
    .status-error {
        background-color: #FFEBEE;
        color: #C62828;
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

def load_settings():
    """Load user settings from JSON file"""
    default_settings = {
        "appearance": {
            "theme": "Light",
            "accent_color": "Blue",
            "chart_style": "Modern",
            "sidebar_expanded": True
        },
        "data": {
            "auto_refresh": True,
            "refresh_interval": 60,
            "cache_data": True,
            "max_cache_age": 24,
            "data_sources": ["NBA API", "Basketball Reference"]
        },
        "notifications": {
            "enable_notifications": True,
            "injury_alerts": True,
            "game_reminders": False,
            "performance_milestones": True
        },
        "defaults": {
            "favorite_team": "Boston Celtics",
            "favorite_players": ["Jayson Tatum", "Jaylen Brown"],
            "default_view": "Player Dashboard"
        },
        "system": {
            "debug_mode": False,
            "log_level": "INFO",
            "use_advanced_stats": True,
            "api_timeout": 30,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                user_settings = json.load(f)
                
            # Update default settings with user settings (preserves new settings not in user file)
            for category in default_settings:
                if category in user_settings:
                    for setting in default_settings[category]:
                        if setting in user_settings[category]:
                            default_settings[category][setting] = user_settings[category][setting]
                            
            return default_settings
        except Exception as e:
            module_logger.error(f"Error loading settings: {str(e)}")
            return default_settings
    else:
        return default_settings

def save_settings(settings):
    """Save user settings to JSON file"""
    try:
        # Update last updated timestamp
        settings["system"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        
        module_logger.info("Settings saved successfully")
        return True
    except Exception as e:
        module_logger.error(f"Error saving settings: {str(e)}")
        return False

def appearance_settings(settings):
    """Render appearance settings section"""
    st.markdown('<div class="settings-header">Appearance Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-description">Customize the look and feel of the SportsIQ application</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "Application Theme",
            ["Light", "Dark", "System Default"],
            index=["Light", "Dark", "System Default"].index(settings["appearance"]["theme"])
        )
        settings["appearance"]["theme"] = theme
        
        accent_color = st.selectbox(
            "Accent Color",
            ["Blue", "Green", "Red", "Purple", "Orange"],
            index=["Blue", "Green", "Red", "Purple", "Orange"].index(settings["appearance"]["accent_color"])
        )
        settings["appearance"]["accent_color"] = accent_color
        
    with col2:
        chart_style = st.selectbox(
            "Chart Style",
            ["Modern", "Classic", "Minimal", "Colorful"],
            index=["Modern", "Classic", "Minimal", "Colorful"].index(settings["appearance"]["chart_style"])
        )
        settings["appearance"]["chart_style"] = chart_style
        
        sidebar_expanded = st.checkbox(
            "Start with sidebar expanded",
            value=settings["appearance"]["sidebar_expanded"]
        )
        settings["appearance"]["sidebar_expanded"] = sidebar_expanded
    
    st.markdown("---")
    return settings

def data_settings(settings):
    """Render data settings section"""
    st.markdown('<div class="settings-header">Data Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-description">Configure how data is loaded, refreshed, and cached</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_refresh = st.checkbox(
            "Auto-refresh data",
            value=settings["data"]["auto_refresh"],
            help="Automatically refresh data at specified intervals"
        )
        settings["data"]["auto_refresh"] = auto_refresh
        
        if auto_refresh:
            refresh_interval = st.slider(
                "Refresh Interval (minutes)",
                min_value=15,
                max_value=240,
                value=settings["data"]["refresh_interval"],
                step=15,
                help="How often to refresh data automatically"
            )
            settings["data"]["refresh_interval"] = refresh_interval
        
        cache_data = st.checkbox(
            "Cache data locally",
            value=settings["data"]["cache_data"],
            help="Store data locally to improve performance"
        )
        settings["data"]["cache_data"] = cache_data
        
    with col2:
        if cache_data:
            max_cache_age = st.slider(
                "Maximum Cache Age (hours)",
                min_value=1,
                max_value=72,
                value=settings["data"]["max_cache_age"],
                step=1,
                help="Maximum age of cached data before refreshing"
            )
            settings["data"]["max_cache_age"] = max_cache_age
        
        data_sources = st.multiselect(
            "Data Sources",
            ["NBA API", "Basketball Reference", "Sports Radar", "Stats.NBA.com"],
            default=settings["data"]["data_sources"],
            help="Select which data sources to use"
        )
        settings["data"]["data_sources"] = data_sources
        
        if st.button("Clear Cache", help="Delete all cached data and fetch fresh data on next load"):
            st.success("Cache cleared successfully")
            module_logger.info("User cleared cache")
    
    st.markdown("---")
    return settings

def notification_settings(settings):
    """Render notification settings section"""
    st.markdown('<div class="settings-header">Notification Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-description">Configure alerts and notifications for important events</div>', unsafe_allow_html=True)
    
    enable_notifications = st.checkbox(
        "Enable Notifications",
        value=settings["notifications"]["enable_notifications"],
        help="Master switch for all notifications"
    )
    settings["notifications"]["enable_notifications"] = enable_notifications
    
    if enable_notifications:
        col1, col2 = st.columns(2)
        
        with col1:
            injury_alerts = st.checkbox(
                "Injury Alerts",
                value=settings["notifications"]["injury_alerts"],
                help="Get notified about player injuries"
            )
            settings["notifications"]["injury_alerts"] = injury_alerts
            
            game_reminders = st.checkbox(
                "Game Reminders",
                value=settings["notifications"]["game_reminders"],
                help="Get reminders before games start"
            )
            settings["notifications"]["game_reminders"] = game_reminders
            
        with col2:
            performance_milestones = st.checkbox(
                "Performance Milestones",
                value=settings["notifications"]["performance_milestones"],
                help="Get notified when players reach statistical milestones"
            )
            settings["notifications"]["performance_milestones"] = performance_milestones
    
    st.markdown("---")
    return settings

def default_settings(settings):
    """Render default settings section"""
    st.markdown('<div class="settings-header">Default Preferences</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-description">Set your favorite teams, players, and default views</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    nba_teams = [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
        "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
        "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
        "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
        "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
        "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
        "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
        "Utah Jazz", "Washington Wizards"
    ]
    
    nba_players = [
        "LeBron James", "Kevin Durant", "Stephen Curry", "Giannis Antetokounmpo",
        "Nikola Jokić", "Joel Embiid", "Jayson Tatum", "Luka Dončić",
        "Jaylen Brown", "Zion Williamson", "Damian Lillard", "Kyrie Irving",
        "Anthony Davis", "Jimmy Butler", "Bam Adebayo", "Trae Young",
        "Devin Booker", "Anthony Edwards", "Ja Morant", "Shai Gilgeous-Alexander"
    ]
    
    with col1:
        favorite_team = st.selectbox(
            "Favorite Team",
            nba_teams,
            index=nba_teams.index(settings["defaults"]["favorite_team"]) if settings["defaults"]["favorite_team"] in nba_teams else 0
        )
        settings["defaults"]["favorite_team"] = favorite_team
        
        favorite_players = st.multiselect(
            "Favorite Players",
            nba_players,
            default=[player for player in settings["defaults"]["favorite_players"] if player in nba_players]
        )
        settings["defaults"]["favorite_players"] = favorite_players
        
    with col2:
        default_view = st.selectbox(
            "Default Landing Page",
            ["Home", "Player Dashboard", "Injury Risk", "Team Analysis", "Game Prediction"],
            index=["Home", "Player Dashboard", "Injury Risk", "Team Analysis", "Game Prediction"].index(settings["defaults"]["default_view"]) if settings["defaults"]["default_view"] in ["Home", "Player Dashboard", "Injury Risk", "Team Analysis", "Game Prediction"] else 0
        )
        settings["defaults"]["default_view"] = default_view
    
    st.markdown("---")
    return settings

def system_settings(settings):
    """Render system settings section"""
    st.markdown('<div class="settings-header">System Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-description">Advanced settings for application behavior and performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        debug_mode = st.checkbox(
            "Debug Mode",
            value=settings["system"]["debug_mode"],
            help="Enable detailed logging and debugging information"
        )
        settings["system"]["debug_mode"] = debug_mode
        
        log_level = st.selectbox(
            "Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"].index(settings["system"]["log_level"])
        )
        settings["system"]["log_level"] = log_level
        
    with col2:
        use_advanced_stats = st.checkbox(
            "Use Advanced Statistics",
            value=settings["system"]["use_advanced_stats"],
            help="Enable the use of advanced basketball statistics and metrics"
        )
        settings["system"]["use_advanced_stats"] = use_advanced_stats
        
        api_timeout = st.slider(
            "API Timeout (seconds)",
            min_value=5,
            max_value=120,
            value=settings["system"]["api_timeout"],
            step=5,
            help="Maximum time to wait for API responses"
        )
        settings["system"]["api_timeout"] = api_timeout
    
    # Display last updated timestamp
    st.info(f"Settings last updated: {settings['system']['last_updated']}")
    
    return settings

def main():
    st.markdown('<div class="page-title">Application Settings</div>', unsafe_allow_html=True)
    
    # Load current settings
    settings = load_settings()
    
    # Create tabs for different settings categories
    tabs = st.tabs(["Appearance", "Data", "Notifications", "Defaults", "System"])
    
    with tabs[0]:
        settings = appearance_settings(settings)
        
    with tabs[1]:
        settings = data_settings(settings)
        
    with tabs[2]:
        settings = notification_settings(settings)
        
    with tabs[3]:
        settings = default_settings(settings)
        
    with tabs[4]:
        settings = system_settings(settings)
    
    # Save settings button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("Save Settings", use_container_width=True):
            success = save_settings(settings)
            if success:
                st.markdown('<div class="status-box status-success">Settings saved successfully!</div>', unsafe_allow_html=True)
                module_logger.info("User saved settings")
            else:
                st.markdown('<div class="status-box status-error">Error saving settings. Please try again.</div>', unsafe_allow_html=True)
                module_logger.error("Error occurred while saving settings")
    
    # Reset to defaults button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Reset to Defaults", use_container_width=True):
            if os.path.exists(SETTINGS_FILE):
                try:
                    os.remove(SETTINGS_FILE)
                    st.markdown('<div class="status-box status-success">Settings reset to defaults. Refresh the page to see changes.</div>', unsafe_allow_html=True)
                    module_logger.info("User reset settings to defaults")
                except Exception as e:
                    st.markdown('<div class="status-box status-error">Error resetting settings. Please try again.</div>', unsafe_allow_html=True)
                    module_logger.error(f"Error resetting settings: {str(e)}")
            else:
                st.markdown('<div class="status-box status-warning">Already using default settings.</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        Settings are stored locally and will persist between sessions. 
        Some settings may require application restart to take effect.
    </div>
    """, unsafe_allow_html=True)
    
    # Log page view
    module_logger.info("User viewed Settings page")

if __name__ == "__main__":
    main() 