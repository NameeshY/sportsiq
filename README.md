# SportsIQ 🏀



SportsIQ is a comprehensive NBA analytics dashboard that provides real-time insights and advanced statistics for basketball teams and players. The application combines data from multiple sources with machine learning models to deliver predictive analytics and stunning visualizations.

## 🌟 Features

- **Player Performance Dashboard**: Track player statistics, visualize performance trends, and discover insights

<img width="1790" alt="Screenshot 2025-03-28 at 9 52 28 PM" src="https://github.com/user-attachments/assets/4143b05c-2df8-4db7-989e-6509bcf69cab" />

- **Injury Risk Analysis**: Assess player fatigue and injury risk based on workload analysis

<img width="1792" alt="Screenshot 2025-03-28 at 9 51 12 PM" src="https://github.com/user-attachments/assets/c33e8319-87a5-42cc-ab13-3dcfa4dac0f9" />

<img width="1792" alt="Screenshot 2025-03-28 at 9 50 52 PM" src="https://github.com/user-attachments/assets/53daf398-4787-4a38-8829-f8514952d5a0" />

- **Team Analysis**: Analyze team performance metrics and lineup effectiveness

<img width="1792" alt="Screenshot 2025-03-28 at 9 53 36 PM" src="https://github.com/user-attachments/assets/6b269053-44b9-407a-8f06-b5fa226ca387" />

- **Game Prediction**: Predict game outcomes with machine learning models

 <img width="1792" alt="Screenshot 2025-03-28 at 9 54 32 PM" src="https://github.com/user-attachments/assets/eaccbed0-b715-40cc-bca6-8b5fd78250d4" />

- **Interactive Visualizations**: Explore data through dynamic, interactive charts
- **API Access**: Programmatically access NBA data and analytics

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Dependencies](#-dependencies)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

Clone the repository and run the application:

```bash
# Clone the repository
git clone https://github.com/NameeshY/sportsiq.git
cd sportsiq

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_app.py
```

The application will be available at [http://localhost:8501](http://localhost:8501)

## 📥 Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/NameeshY/sportsiq.git
cd sportsiq
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate the environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root or copy the example:

```bash
cp example.env .env
```

Edit the `.env` file with your configuration:

```
# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sportsiq
DB_USER=your_username
DB_PASSWORD=your_password

# API settings
NBA_API_KEY=your_api_key_here

# Application settings
DEBUG=True
LOG_LEVEL=INFO
```

### Step 5: Set Up the Database

Create a PostgreSQL database named `sportsiq`:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE sportsiq;

# Exit PostgreSQL
\q
```

### Step 6: Run the Application

```bash
python run_app.py
```

For advanced options:

```bash
python run_app.py --port 8501 --debug
```

## 📂 Project Structure

```
sportsiq/
├── app.py                 # Main Streamlit application
├── run_app.py             # Application launcher
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (create this file)
├── README.md              # Project documentation
├── cache/                 # Cached data
├── config/                # Configuration files
├── data/                  # Data files
│   ├── raw/               # Raw data
│   └── processed/         # Processed data
├── models/                # Machine learning models
├── notebooks/             # Jupyter notebooks for exploration
│   └── README.md          # Notebook documentation
├── pages/                 # Streamlit pages
│   ├── 1_Player_Dashboard.py
│   ├── 2_Injury_Risk.py
│   ├── 3_Team_Analysis.py
│   ├── 4_Game_Prediction.py
│   ├── 5_About.py
│   ├── 6_Settings.py
│   └── 7_API.py
└── utils/                 # Utility modules
    ├── __init__.py
    ├── db_utils.py        # Database utilities
    ├── env_utils.py       # Environment utilities
    ├── log_utils.py       # Logging utilities
    ├── nba_loader.py      # NBA data loader
    ├── visualization.py   # Visualization helpers
    └── models.py          # ML model utilities
```

## 🎮 Usage Guide

### 1. Home Dashboard

The home page provides an overview of the application with key metrics and navigation to other sections.

### 2. Player Performance Dashboard

Track and analyze individual player performance:

- Select players to view their statistics
- Visualize performance trends over time
- Compare players across different metrics
- Get AI-generated insights about player performance

### 3. Injury Risk Analysis

Assess player injury risk and fatigue:

- View player fatigue metrics and workload factors
- See risk probability based on multiple factors
- Get recommendations for load management
- Track recent minutes and games played

### 4. Team Analysis

Analyze team performance and lineups:

- Compare team statistics and rankings
- Analyze lineup effectiveness
- View offensive and defensive ratings
- Discover optimal player combinations

### 5. Game Prediction

Predict game outcomes with machine learning:

- Select matchups to analyze
- View win probability for both teams
- Identify key factors influencing the outcome
- See predicted scores and confidence levels

### 6. Settings

Configure application preferences:

- Appearance settings
- Data refresh options
- Notification preferences
- Default teams and players

### 7. API Documentation

Learn how to access SportsIQ data programmatically:

- API endpoints documentation
- Authentication information
- Code examples in multiple languages
- Rate limits and error codes

## 🔌 API Documentation

SportsIQ provides a RESTful API for programmatic access to data and analytics. For detailed API documentation, visit the API page in the application or refer to our [API Documentation](https://github.com/NameeshY/sportsiq/wiki/API).

Key endpoints include:

- `/api/v1/players` - Access player data
- `/api/v1/teams` - Access team data
- `/api/v1/games` - Access game data
- `/api/v1/stats` - Access statistical data
- `/api/v1/predictions` - Access predictions and analytics

## 📚 Dependencies

SportsIQ relies on the following key libraries:

- **Streamlit**: Web application framework
- **Pandas & NumPy**: Data processing and analysis
- **Plotly & Matplotlib**: Data visualization
- **SQLAlchemy**: Database ORM
- **Scikit-learn**: Machine learning algorithms
- **Python-dotenv**: Environment variable management

For a complete list of dependencies, see [requirements.txt](requirements.txt).

## 🛠️ Development

### Setting Up Development Environment

Follow the installation steps, then:

```bash
# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Style

We use [Black](https://github.com/psf/black) for code formatting:

```bash
# Format code
black .
```

### Testing

Run tests using pytest:

```bash
pytest
```

### Building Documentation

Documentation is built using Sphinx:

```bash
cd docs
make html
```

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure your code follows our coding standards and includes appropriate tests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Data Sources

- [NBA API](https://github.com/swar/nba_api)
- [Basketball Reference](https://www.basketball-reference.com/)
- [Stats.NBA.com](https://stats.nba.com/)

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Plotly](https://plotly.com/) for interactive visualizations
- All contributors and open-source projects that made this possible

---

Built with ❤️ by [NameeshY](https://github.com/NameeshY)

For questions, feedback, or support, please [open an issue](https://github.com/NameeshY/sportsiq/issues).
