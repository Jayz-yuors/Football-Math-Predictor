# ⚽ Football Match Predictor (ML-Based League Simulation)

An end-to-end **machine learning system** that predicts football match outcomes and simulates **live league tables** based on upcoming matchdays.

The project combines:
- Historical match data
- Team & player-level features
- League table dynamics
- Trained XGBoost models per league
- Live fixtures and real-time table updates

It supports **multiple European leagues**:
- Premier League (PL)
- La Liga (PD)
- Serie A (SA)
- Bundesliga (BL1)
- Ligue 1 (FL1)

---

## 🚀 Project Overview

This project predicts the probabilities of:
- **Home Win**
- **Draw**
- **Away Win**

for upcoming fixtures and then **simulates the entire matchday** (typically 3–4 days) to show how the **league table would change** if those matches were played.

### 🔑 Key Highlights
- League-specific ML models
- Matchday-based simulation window
- Automatically updated league tables
- Clean CLI-based workflow
- Reusable datasets for research and experimentation

---

## 📂 Core Datasets (`data_exports/`)

All **processed datasets** are already provided so users can:
- Train models immediately
- Build their own prediction pipelines
- Experiment with different features and algorithms

---

### 1️⃣ `matches_unified.csv`

**Sources**
- Kaggle (historical football datasets)
- football-data.org API

**Description**
- Match-level historical data
- Home & away teams
- Final scores
- Match dates
- Competition codes

**Why it matters**
- Primary dataset for training outcome prediction
- Used to generate labels: `home_win / draw / away_win`

---

### 2️⃣ `player_data.csv`

**Sources**
- Understat
- Kaggle player datasets

**Description**
- Player-level performance metrics
- Goals, xG, assists, minutes played

**Why it matters**
- Enhances team strength estimation
- Helps quantify attacking and defensive power

---

### 3️⃣ `fixtures_current_season.csv`

**Source**
- football-data.org API

**Description**
- Upcoming fixtures
- Match dates
- Match status (`SCHEDULED`, `TIMED`, `FINISHED`)

**Why it matters**
- Drives live predictions
- Enables matchday simulation logic

---

### 4️⃣ `team_player_features.csv`

**Sources**
- Aggregated from Understat + historical match data

**Description**
- Team-level features derived from players
- Attack strength
- Defensive stability
- Recent form indicators

**Why it matters**
- Core feature set used by ML models
- Improves prediction realism and stability

---

> ⚠️ **IMPORTANT**  
> **You can directly use the datasets in `data_exports/` to build and train your own models or experiment with alternative ML approaches.**

---
**🛠 Feature Engineering**
The core logic resides in model/feature_engineering/. Features include:

League table position
Goal difference
Team form
Head-to-head trends
Team and player strength indicators

✅ Design Guarantees
No data leakage
Identical features for training and inference
League-agnostic feature generation

🤖 Model Training
Each league has its own trained XGBoost model stored in trained_models/:
PL_model.joblib (Premier League)
PD_model.joblib (La Liga)
SA_model.joblib (Serie A)
BL1_model.joblib (Bundesliga)
FL1_model.joblib (Ligue 1)

🔍 Algorithm Details
XGBoost (Multi-class classification)
Predicts probabilities for: Home Win, Draw, or Away Win.
--- 
---
**⚙️ Installation & Setup**
---
1️⃣ Clone the Repository
Bash
git clone https://github.com/Jayz-yuors/Football-Match-Predictor.git
cd Football-Match-Predictor
---
2️⃣ Create Virtual Environment
Bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
---
3️⃣ Install Dependencies
Bash
pip install -r requirements.txt
---
4️⃣ Set API Key
Bash
export FOOTBALL_DATA_API_KEY=your_api_key_here
🏋️ Training Models (Optional)
Models are already trained, but you can retrain them using:
Bash
python -m model.training.train_model
Premier League model is already trained.
Other leagues are trained automatically.
---
▶️ Running Predictions
Bash
python -m run_prediction
🔁 Execution Flow
Select league
View upcoming matchday fixtures
Choose a fixture
Get match outcome probabilities
View:
Current league table
League table after matchday simulation
🖥️ Sample Output
📅 Matchday Fixtures
🔮 Match Prediction
📊 League Table Simulation
📈 Why This Project Matters
---
📌 Applications
Sports analytics
Betting and odds research
Match outcome forecasting
League performance simulation
Feature engineering experimentation
---
💪 Strengths
Fully modular architecture
Multi-league scalability
Clean separation of data, features, and inference
Realistic league evolution modeling
---
📜 License
This project is released under the MIT License. You are free to use, modify, and distribute it with attribution.
---
🙌 Author
Jay Keluskar Computer Engineering Student
ML • Data • Sports Analytics
Would you like me to add a "Project Structure" section to show how the folders are organized?
