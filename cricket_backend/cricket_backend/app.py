from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np

app = FastAPI()

# Enable CORS for the frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://silly-mermaid-968230.netlify.app"],  # Allows requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

from pydantic import BaseModel

class PitchAnalysisRequest(BaseModel):
    pitch_report: str
    player_names: list[str]

@app.post("/analyze_pitch")
async def analyze_pitch_and_select_players(request: PitchAnalysisRequest):
    # Analyze the pitch conditions using the pitch report
    pitch_type = determine_pitch_type(request.pitch_report)

    # Use the pitch summary information to inform the decision-making process
    selected_players = select_best_players(pitch_type, request.player_names)

    # Designate a captain and vice-captain from the selected players
    captain, vice_captain = designate_captains(selected_players)

    # Return the selected players, captain, and vice-captain
    return {"selected_players": selected_players, "captain": captain, "vice_captain": vice_captain}

def determine_pitch_type(pitch_report: str) -> str:
    if "green" in pitch_report.lower():
        return "green"
    elif "dry" in pitch_report.lower():
        return "dry"
    elif "flat" in pitch_report.lower():
        return "flat"
    elif "dusty" in pitch_report.lower():
        return "dusty"
    elif "wet" in pitch_report.lower():
        return "wet"
    else:
        return "unknown"

def select_best_players(pitch_type: str, player_names: list) -> list:
    # Load player performance data
    player_data = pd.read_csv('player_performance.csv')

    # Encode categorical data
    le = LabelEncoder()
    player_data['PitchType'] = le.fit_transform(player_data['PitchType'])

    # Prepare features and target
    X = player_data.drop(columns=['PlayerName', 'Performance'])
    y = player_data['Performance']

    # Train a Random Forest model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict the best players
    pitch_encoded = le.transform([pitch_type])[0]
    player_features = np.array([[pitch_encoded] * len(player_names)]).T
    predictions = model.predict(player_features)

    # Select top 11 players based on predictions
    top_players_indices = np.argsort(predictions)[-11:]
    selected_players = [player_names[i] for i in top_players_indices if i < len(player_names)]

    # Ensure at least two players are selected
    if len(selected_players) < 2:
        selected_players = player_names[:2] if len(player_names) >= 2 else player_names

    return selected_players

def designate_captains(selected_players: list) -> tuple:
    # Simple heuristic to designate a captain and vice-captain
    if len(selected_players) >= 2:
        return selected_players[0], selected_players[1]
    elif len(selected_players) == 1:
        return selected_players[0], selected_players[0]
    else:
        return None, None
