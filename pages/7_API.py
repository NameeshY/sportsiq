"""
SportsIQ - API Documentation
Provides documentation and examples for the SportsIQ API
"""
import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import utilities and modules
from sportsiq.utils import setup_logging, get_logger

# Set up logging
logger = setup_logging()
module_logger = get_logger("api")

# Set page configuration
st.set_page_config(
    page_title="SportsIQ - API",
    page_icon="🔌",
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
    .api-section {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #1E88E5;
    }
    .endpoint {
        font-family: monospace;
        font-size: 1.1rem;
        font-weight: bold;
        background-color: #e9ecef;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .http-method {
        font-weight: bold;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        color: white;
        display: inline-block;
        width: 60px;
        text-align: center;
        margin-right: 10px;
    }
    .get {
        background-color: #28a745;
    }
    .post {
        background-color: #007bff;
    }
    .put {
        background-color: #fd7e14;
    }
    .delete {
        background-color: #dc3545;
    }
    .code-block {
        background-color: #272822;
        color: #f8f8f2;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        overflow-x: auto;
    }
    .parameter-table {
        width: 100%;
        margin-bottom: 1rem;
    }
    .parameter-table th {
        background-color: #f1f3f5;
        padding: 0.5rem;
        text-align: left;
    }
    .parameter-table td {
        padding: 0.5rem;
        border-bottom: 1px solid #dee2e6;
    }
    .required {
        color: #dc3545;
        font-weight: bold;
    }
    .optional {
        color: #6c757d;
    }
    .api-key-box {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #495057;
    }
    .tab-content {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def generate_api_key():
    """Generate a sample API key for demonstration purposes"""
    import uuid
    return f"sq_{uuid.uuid4().hex[:24]}"

def get_sample_endpoints():
    """Return sample API endpoints and documentation"""
    endpoints = [
        {
            "path": "/api/v1/players",
            "method": "GET",
            "description": "Get a list of all NBA players with basic information",
            "parameters": [
                {"name": "team_id", "type": "integer", "required": False, "description": "Filter players by team ID"},
                {"name": "position", "type": "string", "required": False, "description": "Filter players by position (G, F, C)"},
                {"name": "active", "type": "boolean", "required": False, "description": "Filter by active/inactive status"},
                {"name": "limit", "type": "integer", "required": False, "description": "Maximum number of results to return"}
            ],
            "response": {
                "players": [
                    {
                        "id": 2544,
                        "name": "LeBron James",
                        "team": "Los Angeles Lakers",
                        "position": "F",
                        "jersey_number": "23",
                        "height": "6-9",
                        "weight": "250 lbs",
                        "age": 38,
                        "draft_year": 2003
                    }
                ],
                "metadata": {
                    "total_count": 450,
                    "returned_count": 1,
                    "page": 1
                }
            }
        },
        {
            "path": "/api/v1/players/{player_id}",
            "method": "GET",
            "description": "Get detailed information about a specific player",
            "parameters": [
                {"name": "player_id", "type": "integer", "required": True, "description": "The unique ID of the player"},
                {"name": "include_stats", "type": "boolean", "required": False, "description": "Include player statistics"}
            ],
            "response": {
                "id": 2544,
                "name": "LeBron James",
                "full_name": "LeBron Raymone James Sr.",
                "team": "Los Angeles Lakers",
                "position": "F",
                "jersey_number": "23",
                "height": "6-9",
                "weight": "250 lbs",
                "age": 38,
                "birth_date": "1984-12-30",
                "draft_year": 2003,
                "draft_round": 1,
                "draft_number": 1,
                "college": "St. Vincent-St. Mary HS (OH)",
                "country": "USA",
                "seasons_in_league": 20,
                "stats": {
                    "current_season": {
                        "games_played": 55,
                        "games_started": 54,
                        "minutes_per_game": 35.5,
                        "points_per_game": 25.7,
                        "rebounds_per_game": 7.3,
                        "assists_per_game": 8.1,
                        "steals_per_game": 1.3,
                        "blocks_per_game": 0.5,
                        "field_goal_percentage": 0.507,
                        "three_point_percentage": 0.315,
                        "free_throw_percentage": 0.761
                    }
                }
            }
        },
        {
            "path": "/api/v1/teams",
            "method": "GET",
            "description": "Get a list of all NBA teams with basic information",
            "parameters": [
                {"name": "conference", "type": "string", "required": False, "description": "Filter by conference (East, West)"},
                {"name": "division", "type": "string", "required": False, "description": "Filter by division name"}
            ],
            "response": {
                "teams": [
                    {
                        "id": 1610612747,
                        "name": "Los Angeles Lakers",
                        "abbreviation": "LAL",
                        "nickname": "Lakers",
                        "city": "Los Angeles",
                        "state": "California",
                        "conference": "West",
                        "division": "Pacific"
                    }
                ],
                "metadata": {
                    "total_count": 30,
                    "returned_count": 1
                }
            }
        },
        {
            "path": "/api/v1/games",
            "method": "GET",
            "description": "Get a list of games with filters",
            "parameters": [
                {"name": "team_id", "type": "integer", "required": False, "description": "Filter games by team ID"},
                {"name": "season", "type": "string", "required": False, "description": "Season in format YYYY-YY (e.g., 2022-23)"},
                {"name": "start_date", "type": "string", "required": False, "description": "Filter games on or after this date (YYYY-MM-DD)"},
                {"name": "end_date", "type": "string", "required": False, "description": "Filter games on or before this date (YYYY-MM-DD)"},
                {"name": "limit", "type": "integer", "required": False, "description": "Maximum number of results to return"}
            ],
            "response": {
                "games": [
                    {
                        "id": 22200123,
                        "season": "2022-23",
                        "date": "2023-01-15",
                        "home_team": {
                            "id": 1610612747,
                            "name": "Los Angeles Lakers",
                            "abbreviation": "LAL",
                            "score": 112
                        },
                        "away_team": {
                            "id": 1610612755,
                            "name": "Philadelphia 76ers",
                            "abbreviation": "PHI",
                            "score": 113
                        },
                        "status": "Final",
                        "arena": "Crypto.com Arena",
                        "city": "Los Angeles",
                        "state": "CA"
                    }
                ],
                "metadata": {
                    "total_count": 1230,
                    "returned_count": 1,
                    "page": 1
                }
            }
        },
        {
            "path": "/api/v1/stats/player/{player_id}",
            "method": "GET",
            "description": "Get comprehensive statistics for a player",
            "parameters": [
                {"name": "player_id", "type": "integer", "required": True, "description": "The unique ID of the player"},
                {"name": "season", "type": "string", "required": False, "description": "Season in format YYYY-YY (e.g., 2022-23)"},
                {"name": "per_mode", "type": "string", "required": False, "description": "Stat calculation mode (Totals, PerGame, Per36)"},
                {"name": "include_advanced", "type": "boolean", "required": False, "description": "Include advanced statistics"}
            ],
            "response": {
                "player_id": 2544,
                "name": "LeBron James",
                "team": "Los Angeles Lakers",
                "season": "2022-23",
                "per_mode": "PerGame",
                "stats": {
                    "games_played": 55,
                    "minutes_per_game": 35.5,
                    "points": 25.7,
                    "assists": 8.1,
                    "rebounds": 7.3,
                    "steals": 1.3,
                    "blocks": 0.5,
                    "turnovers": 3.2,
                    "field_goals_made": 10.2,
                    "field_goals_attempted": 20.1,
                    "field_goal_percentage": 0.507,
                    "three_pointers_made": 2.1,
                    "three_pointers_attempted": 6.8,
                    "three_point_percentage": 0.315,
                    "free_throws_made": 3.2,
                    "free_throws_attempted": 4.2,
                    "free_throw_percentage": 0.761
                },
                "advanced_stats": {
                    "player_efficiency_rating": 24.5,
                    "true_shooting_percentage": 0.558,
                    "usage_percentage": 31.2,
                    "offensive_rebound_percentage": 3.5,
                    "defensive_rebound_percentage": 17.8,
                    "total_rebound_percentage": 10.8,
                    "assist_percentage": 36.2,
                    "steal_percentage": 1.8,
                    "block_percentage": 1.2,
                    "turnover_percentage": 12.5,
                    "offensive_rating": 113.7,
                    "defensive_rating": 112.8,
                    "net_rating": 0.9,
                    "box_plus_minus": 5.3,
                    "value_over_replacement_player": 4.2
                }
            }
        },
        {
            "path": "/api/v1/predictions/injury-risk",
            "method": "GET",
            "description": "Get injury risk assessment for a player",
            "parameters": [
                {"name": "player_id", "type": "integer", "required": True, "description": "The unique ID of the player"}
            ],
            "response": {
                "player_id": 2544,
                "name": "LeBron James",
                "risk_assessment": {
                    "overall_risk": "Medium",
                    "probability": 0.35,
                    "fatigue_score": 62.4,
                    "workload_index": 78.3,
                    "recent_minutes": "High",
                    "back_to_back_games": "Yes",
                    "days_of_rest": 1,
                    "games_last_7_days": 3,
                    "injury_history_factor": "Medium"
                },
                "recommendations": [
                    "Consider load management in upcoming back-to-back games",
                    "Monitor minutes in the next game",
                    "Focus on recovery protocols"
                ]
            }
        },
        {
            "path": "/api/v1/predictions/game",
            "method": "GET",
            "description": "Get prediction for a game outcome",
            "parameters": [
                {"name": "home_team_id", "type": "integer", "required": True, "description": "Home team ID"},
                {"name": "away_team_id", "type": "integer", "required": True, "description": "Away team ID"}
            ],
            "response": {
                "game_prediction": {
                    "home_team": {
                        "id": 1610612747,
                        "name": "Los Angeles Lakers",
                        "win_probability": 0.58,
                        "predicted_score": 112.5
                    },
                    "away_team": {
                        "id": 1610612755,
                        "name": "Philadelphia 76ers",
                        "win_probability": 0.42,
                        "predicted_score": 108.2
                    },
                    "key_factors": [
                        "Home court advantage",
                        "Recent offensive performance of Lakers",
                        "76ers' road record",
                        "Matchup advantages in frontcourt"
                    ],
                    "confidence": "Medium"
                }
            }
        }
    ]
    
    return endpoints

def language_tab(language, endpoint):
    """Display code examples for different languages"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sq_1234567890abcdef1234567890"
    }
    
    base_url = "https://api.sportsiq-analytics.com"
    full_url = f"{base_url}{endpoint['path']}"
    
    if language == "curl":
        params = ""
        for param in endpoint["parameters"]:
            if not param["required"]:
                params += f" \\\n    --data-urlencode '{param['name']}=value'"
                
        if "{player_id}" in endpoint["path"]:
            full_url = full_url.replace("{player_id}", "2544")
        
        code = f"""curl -X {endpoint['method']} "{full_url}" \\
    -H "Content-Type: application/json" \\
    -H "Authorization: Bearer sq_1234567890abcdef1234567890"{params}"""
        
    elif language == "python":
        params = "{"
        for i, param in enumerate(endpoint["parameters"]):
            if not param["required"] or "{player_id}" in endpoint["path"] and param["name"] == "player_id":
                if i > 0 and params != "{":
                    params += ", "
                value = "2544" if param["name"] == "player_id" else "value"
                params += f'"{param["name"]}": "{value}"'
        params += "}"
        
        url = full_url
        if "{player_id}" in endpoint["path"]:
            url = full_url.replace("{player_id}", "2544")
        
        code = f"""import requests

url = "{url}"
headers = {{
    "Content-Type": "application/json",
    "Authorization": "Bearer sq_1234567890abcdef1234567890"
}}
params = {params}

response = requests.{endpoint['method'].lower()}(url, headers=headers, params=params)
data = response.json()

print(data)"""
        
    elif language == "javascript":
        params = "{"
        for i, param in enumerate(endpoint["parameters"]):
            if not param["required"] or "{player_id}" in endpoint["path"] and param["name"] == "player_id":
                if i > 0 and params != "{":
                    params += ", "
                value = "2544" if param["name"] == "player_id" else "value"
                params += f'"{param["name"]}": "{value}"'
        params += "}"
        
        url = full_url
        if "{player_id}" in endpoint["path"]:
            url = full_url.replace("{player_id}", "2544")
            
        code = f"""// Using fetch API
const url = '{url}';
const headers = {{
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sq_1234567890abcdef1234567890'
}};

// Create URL with query parameters
const params = {params};
const queryString = new URLSearchParams(params).toString();
const requestUrl = url + '?' + queryString;

fetch(requestUrl, {{
    method: '{endpoint['method']}',
    headers: headers
}})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));"""
    
    return code

def display_endpoint(endpoint):
    """Display detailed information about an API endpoint"""
    method_class = endpoint["method"].lower()
    
    st.markdown(f"""
    <div class="api-section">
        <div class="endpoint">
            <span class="http-method {method_class}">{endpoint["method"]}</span> {endpoint["path"]}
        </div>
        <p>{endpoint["description"]}</p>
        
        <h4>Parameters</h4>
        <table class="parameter-table">
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
            </tr>
    """, unsafe_allow_html=True)
    
    for param in endpoint["parameters"]:
        required_class = "required" if param["required"] else "optional"
        required_text = "Yes" if param["required"] else "No"
        
        st.markdown(f"""
            <tr>
                <td><code>{param["name"]}</code></td>
                <td>{param["type"]}</td>
                <td class="{required_class}">{required_text}</td>
                <td>{param["description"]}</td>
            </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("</table>", unsafe_allow_html=True)
    
    st.markdown("<h4>Example Response</h4>", unsafe_allow_html=True)
    
    response_json = json.dumps(endpoint["response"], indent=2)
    st.code(response_json, language="json")
    
    st.markdown("<h4>Code Examples</h4>", unsafe_allow_html=True)
    
    # Create tabs for different languages
    lang_tabs = st.tabs(["cURL", "Python", "JavaScript"])
    
    with lang_tabs[0]:
        st.code(language_tab("curl", endpoint), language="bash")
        
    with lang_tabs[1]:
        st.code(language_tab("python", endpoint), language="python")
        
    with lang_tabs[2]:
        st.code(language_tab("javascript", endpoint), language="javascript")
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Page title
    st.markdown('<div class="page-title">SportsIQ API Documentation</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to the SportsIQ API documentation. This API provides programmatic access to NBA data, 
    analytics, and predictive models. Use this API to integrate SportsIQ analytics into your own 
    applications, websites, or data pipelines.
    
    All API endpoints require authentication with an API key, which you can obtain by signing up for 
    a SportsIQ developer account.
    """)
    
    # API Key Management
    st.markdown('<div class="section-title">API Key Authentication</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        All API requests must include an authorization header with your API key:
        
        ```
        Authorization: Bearer YOUR_API_KEY
        ```
        
        API keys are tied to your SportsIQ account and have usage limitations based on your subscription tier.
        Keep your API key secure and do not share it publicly.
        """)
    
    with col2:
        st.markdown('<div class="api-key-box">', unsafe_allow_html=True)
        sample_key = generate_api_key()
        st.code(sample_key, language=None)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Generate Sample API Key"):
            st.experimental_rerun()
    
    # Rate Limits
    st.markdown('<div class="section-title">Rate Limits</div>', unsafe_allow_html=True)
    
    rate_limits = pd.DataFrame({
        "Plan": ["Free", "Basic", "Premium", "Enterprise"],
        "Requests per Minute": [10, 30, 100, 500],
        "Requests per Day": [100, 5000, 50000, "Unlimited"],
        "Data Freshness": ["24 hours", "6 hours", "1 hour", "Real-time"]
    })
    
    st.table(rate_limits)
    
    # Endpoints
    st.markdown('<div class="section-title">API Endpoints</div>', unsafe_allow_html=True)
    
    endpoints = get_sample_endpoints()
    
    # Group endpoints by category
    endpoint_categories = {
        "Players": [ep for ep in endpoints if "/players" in ep["path"]],
        "Teams": [ep for ep in endpoints if "/teams" in ep["path"]],
        "Games": [ep for ep in endpoints if "/games" in ep["path"]],
        "Statistics": [ep for ep in endpoints if "/stats" in ep["path"]],
        "Predictions": [ep for ep in endpoints if "/predictions" in ep["path"]]
    }
    
    # Create tabs for different endpoint categories
    endpoint_tabs = st.tabs(list(endpoint_categories.keys()))
    
    for i, (category, category_endpoints) in enumerate(endpoint_categories.items()):
        with endpoint_tabs[i]:
            for endpoint in category_endpoints:
                display_endpoint(endpoint)
    
    # Error Codes
    st.markdown('<div class="section-title">Error Codes</div>', unsafe_allow_html=True)
    
    error_codes = pd.DataFrame({
        "Status Code": [400, 401, 403, 404, 429, 500, 503],
        "Error": [
            "Bad Request", 
            "Unauthorized", 
            "Forbidden", 
            "Not Found", 
            "Too Many Requests", 
            "Internal Server Error",
            "Service Unavailable"
        ],
        "Description": [
            "The request was malformed or contains invalid parameters",
            "API key is missing or invalid",
            "The API key doesn't have access to the requested resource",
            "The requested resource was not found",
            "Rate limit exceeded",
            "An unexpected error occurred on the server",
            "The service is temporarily unavailable"
        ]
    })
    
    st.table(error_codes)
    
    # Request Example
    st.markdown('<div class="section-title">Complete Request Example</div>', unsafe_allow_html=True)
    
    example_code = """
import requests
import json

# API Configuration
API_KEY = 'sq_1234567890abcdef1234567890'
BASE_URL = 'https://api.sportsiq-analytics.com'

# Set up headers with authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# Example 1: Get player statistics
def get_player_stats(player_id, season=None):
    endpoint = f'/api/v1/stats/player/{player_id}'
    params = {}
    if season:
        params['season'] = season
    params['include_advanced'] = 'true'
    
    response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example 2: Get injury risk assessment
def get_injury_risk(player_id):
    endpoint = f'/api/v1/predictions/injury-risk'
    params = {'player_id': player_id}
    
    response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage
if __name__ == "__main__":
    # Get LeBron James' stats for the 2022-23 season
    lebron_stats = get_player_stats(2544, season='2022-23')
    
    if lebron_stats:
        print(f"Points per game: {lebron_stats['stats']['points']}")
        print(f"PER: {lebron_stats['advanced_stats']['player_efficiency_rating']}")
    
    # Get injury risk assessment
    injury_risk = get_injury_risk(2544)
    
    if injury_risk:
        print(f"Risk level: {injury_risk['risk_assessment']['overall_risk']}")
        print(f"Risk probability: {injury_risk['risk_assessment']['probability']}")
        print("Recommendations:")
        for rec in injury_risk['recommendations']:
            print(f"- {rec}")
"""
    
    st.code(example_code, language="python")
    
    # Additional Resources
    st.markdown('<div class="section-title">Additional Resources</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Documentation
        
        * [API Reference Guide](https://example.com/docs)
        * [SDK Documentation](https://example.com/sdk)
        * [Tutorials and Guides](https://example.com/tutorials)
        * [FAQs](https://example.com/faqs)
        
        ### Support
        
        * Email: api-support@sportsiq-analytics.com
        * Discord: [Join our community](https://discord.gg/sportsiq)
        * GitHub: [Issue Tracker](https://github.com/sportsiq/api-issues)
        """)
    
    with col2:
        st.markdown("""
        ### SDKs and Libraries
        
        * [Python SDK](https://github.com/sportsiq/python-sdk)
        * [JavaScript SDK](https://github.com/sportsiq/js-sdk)
        * [R Package](https://github.com/sportsiq/r-package)
        * [Postman Collection](https://github.com/sportsiq/postman)
        
        ### Changelog
        
        * **v1.3.0** (2023-09-01): Added game prediction endpoints
        * **v1.2.0** (2023-06-15): Enhanced player statistics
        * **v1.1.0** (2023-03-10): Added injury risk predictions
        * **v1.0.0** (2023-01-01): Initial API release
        """)
    
    # Log page view
    module_logger.info("User viewed API documentation page")

if __name__ == "__main__":
    main() 