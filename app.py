from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# API credentials
TOKEN_URL = "https://<your-adw-instance>.adb.us-phoenix-1.oraclecloudapps.com/omlusers/api/oauth2/v1/token"
PREDICT_URL = "https://<your-adw-instance>v.adb.us-phoenix-1.oraclecloudapps.com/omlmod/v1/deployment/<your-uri>/score"

# Your attributes
attributes = [
    {"name": "HOME_GAME", "label": "Home Game", "type": "number", "required": True},
    {"name": "TEAM_RESTDAYS", "label": "Team Rest Days", "type": "number", "required": True},
    {"name": "ALLOWED_TWO_POINT_PERCENTAGE", "label": "Allowed Two Point Percentage", "type": "number", "required": True},
    {"name": "ALLOWED_THREE_POINT_PERCENTAGE", "label": "Allowed Three Point Percentage", "type": "number", "required": True},
    {"name": "ALLOWED_POINTS", "label": "Allowed Points", "type": "number", "required": True},
    {"name": "ALLOWED_OFFENSIVE_REBOUNDS", "label": "Allowed Offensive Rebounds", "type": "number", "required": True},
    {"name": "ALLOWED_DEFENSIVE_REBOUNDS", "label": "Allowed Defensive Rebounds", "type": "number", "required": True},
    {"name": "ALLOWED_TOTAL_REBOUNDS", "label": "Allowed Total Rebounds", "type": "number", "required": True},
    {"name": "ALLOWED_STEALS", "label": "Allowed Steals", "type": "number", "required": True},
    {"name": "ALLOWED_BLOCKS", "label": "Allowed Blocks", "type": "number", "required": True},
    {"name": "FORCED_TURNOVERS", "label": "Forced Turnovers", "type": "number", "required": True},
    {"name": "FORCED_FOULS", "label": "Forced Fouls", "type": "number", "required": True},
    {"name": "ALLOWED_POSSESSIONS", "label": "Allowed Possessions", "type": "number", "required": True},
    {"name": "TWO_POINT_PERCENTAGE", "label": "Two Point Percentage", "type": "number", "required": True},
    {"name": "THREE_POINT_PERCENTAGE", "label": "Three Point Percentage", "type": "number", "required": True},
    {"name": "FREE_THROW_PERCENTAGE", "label": "Free Throw Percentage", "type": "number", "required": True},
    {"name": "POINTS", "label": "Points", "type": "number", "required": True},
    {"name": "OFFENSIVE_REBOUNDS", "label": "Offensive Rebounds", "type": "number", "required": True},
    {"name": "DEFENSIVE_REBOUNDS", "label": "Defensive Rebounds", "type": "number", "required": True},
    {"name": "TOTAL_REBOUNDS", "label": "Total Rebounds", "type": "number", "required": True},
    {"name": "STEALS", "label": "Steals", "type": "number", "required": True},
    {"name": "BLOCKS", "label": "Blocks", "type": "number", "required": True},
    {"name": "TURNOVERS", "label": "Turnovers", "type": "number", "required": True},
    {"name": "FOULS", "label": "Fouls", "type": "number", "required": True},
    {"name": "POSSESSIONS", "label": "Possessions", "type": "number", "required": True},
    {"name": "DEFENSIVE_RATING", "label": "Defensive Rating", "type": "number", "required": True},
    {"name": "OFFENSIVE_RATING", "label": "Offensive Rating", "type": "number", "required": True},
    {"name": "OPPONENT_RESTDAYS", "label": "Opponent Rest Days", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_TWO_POINT_PERCENTAGE", "label": "Opponent Allowed Two Point Percentage", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_THREE_POINT_PERCENTAGE", "label": "Opponent Allowed Three Point Percentage", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_POINTS", "label": "Opponent Allowed Points", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_OFFENSIVE_REBOUNDS", "label": "Opponent Allowed Offensive Rebounds", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_DEFENSIVE_REBOUNDS", "label": "Opponent Allowed Defensive Rebounds", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_TOTAL_REBOUNDS", "label": "Opponent Allowed Total Rebounds", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_STEALS", "label": "Opponent Allowed Steals", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_BLOCKS", "label": "Opponent Allowed Blocks", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_FORCED_TURNOVERS", "label": "Opponent Allowed Forced Turnovers", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_FORCED_FOULS", "label": "Opponent Allowed Forced Fouls", "type": "number", "required": True},
    {"name": "OPPONENT_ALLOWED_POSSESSIONS", "label": "Opponent Allowed Possessions", "type": "number", "required": True},
    {"name": "OPPONENT_TWO_POINT_PERCENTAGE", "label": "Opponent Two Point Percentage", "type": "number", "required": True},
    {"name": "OPPONENT_THREE_POINT_PERCENTAGE", "label": "Opponent Three Point Percentage", "type": "number", "required": True},
    {"name": "OPPONENT_FREE_THROW_PERCENTAGE", "label": "Opponent Free Throw Percentage", "type": "number", "required": True},
    {"name": "OPPONENT_POINTS", "label": "Opponent Points", "type": "number", "required": True},
    {"name": "OPPONENT_OFFENSIVE_REBOUNDS", "label": "Opponent Offensive Rebounds", "type": "number", "required": True},
    {"name": "OPPONENT_DEFENSIVE_REBOUNDS", "label": "Opponent Defensive Rebounds", "type": "number", "required": True},
    {"name": "OPPONENT_TOTAL_REBOUNDS", "label": "Opponent Total Rebounds", "type": "number", "required": True},
    {"name": "OPPONENT_STEALS", "label": "Opponent Steals", "type": "number", "required": True},
    {"name": "OPPONENT_BLOCKS", "label": "Opponent Blocks", "type": "number", "required": True},
    {"name": "OPPONENT_TURNOVERS", "label": "Opponent Turnovers", "type": "number", "required": True},
    {"name": "OPPONENT_FOULS", "label": "Opponent Fouls", "type": "number", "required": True},
    {"name": "OPPONENT_POSSESSIONS", "label": "Opponent Possessions", "type": "number", "required": True},
    {"name": "OPPONENT_DEFENSIVE_RATING", "label": "Opponent Defensive Rating", "type": "number", "required": True},
    {"name": "OPPONENT_OFFENSIVE_RATING", "label": "Opponent Offensive Rating", "type": "number", "required": True},
]

# Prepopulate values
prepopulated_values = {
    "HOME_GAME": 0,
    "TEAM_RESTDAYS": 2,
    "ALLOWED_TWO_POINT_PERCENTAGE": 0.495555556,
    "ALLOWED_THREE_POINT_PERCENTAGE": 0.38277512,
    "ALLOWED_POINTS": 107.4615385,
    "ALLOWED_OFFENSIVE_REBOUNDS": 11.53846154,
    "ALLOWED_DEFENSIVE_REBOUNDS": 31.84615385,
    "ALLOWED_TOTAL_REBOUNDS": 43.38461538,
    "ALLOWED_STEALS": 7.230769231,
    "ALLOWED_BLOCKS": 3.846153846,
    "FORCED_TURNOVERS": 14.84615385,
    "FORCED_FOULS": 23.46153846,
    "ALLOWED_POSSESSIONS": 95.26346154,
    "TWO_POINT_PERCENTAGE": 0.49870801,
    "THREE_POINT_PERCENTAGE": 0.333333333,
    "FREE_THROW_PERCENTAGE": 0.779891304,
    "POINTS": 105.6923077,
    "OFFENSIVE_REBOUNDS": 11.69230769,
    "DEFENSIVE_REBOUNDS": 31.15384615,
    "TOTAL_REBOUNDS": 42.84615385,
    "STEALS": 7.923076923,
    "BLOCKS": 7.692307692,
    "TURNOVERS": 15.76923077,
    "FOULS": 23,
    "POSSESSIONS": 93.13846154,
    "DEFENSIVE_RATING": 112.8045703,
    "OFFENSIVE_RATING": 113.4786918,
    "OPPONENT_RESTDAYS": 4,
    "OPPONENT_ALLOWED_TWO_POINT_PERCENTAGE": 0.492021277,
    "OPPONENT_ALLOWED_THREE_POINT_PERCENTAGE": 0.339285714,
    "OPPONENT_ALLOWED_POINTS": 104.5833333,
    "OPPONENT_ALLOWED_OFFENSIVE_REBOUNDS": 12.5,
    "OPPONENT_ALLOWED_DEFENSIVE_REBOUNDS": 31.5,
    "OPPONENT_ALLOWED_TOTAL_REBOUNDS": 44,
    "OPPONENT_ALLOWED_STEALS": 9.25,
    "OPPONENT_ALLOWED_BLOCKS": 4.666666667,
    "OPPONENT_ALLOWED_FORCED_TURNOVERS": 16.16666667,
    "OPPONENT_ALLOWED_FORCED_FOULS": 18.75,
    "OPPONENT_ALLOWED_POSSESSIONS": 92.3125,
    "OPPONENT_TWO_POINT_PERCENTAGE": 0.473225405,
    "OPPONENT_THREE_POINT_PERCENTAGE": 0.389344262,
    "OPPONENT_FREE_THROW_PERCENTAGE": 0.726923077,
    "OPPONENT_POINTS": 102.8333333,
    "OPPONENT_OFFENSIVE_REBOUNDS": 13.83333333,
    "OPPONENT_DEFENSIVE_REBOUNDS": 29.08333333,
    "OPPONENT_TOTAL_REBOUNDS": 42.91666667,
    "OPPONENT_STEALS": 9.75,
    "OPPONENT_BLOCKS": 4.666666667,
    "OPPONENT_TURNOVERS": 15.41666667,
    "OPPONENT_FOULS": 24.75,
    "OPPONENT_POSSESSIONS": 95.95833333,
    "OPPONENT_DEFENSIVE_RATING": 113.2927104,
    "OPPONENT_OFFENSIVE_RATING": 107.164568
}


def get_token():
    response = requests.post(TOKEN_URL, json={
        "grant_type": "password",
        "username": "<user-name>",
        "password": "<password>"
    })

    if response.status_code == 200:
        return response.json()["accessToken"]
    return None

def predict(data):
    token = get_token()
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(PREDICT_URL, headers=headers, json={"inputRecords": [data]})
        return response.json()
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        input_data = {}
        for attr in attributes:
            value = request.form[attr["name"]]

            if attr["type"] == "number":
                input_data[attr["name"]] = float(value) if value else 0.0
            else:
                input_data[attr["name"]] = value
        result = predict(input_data)
        print(result)
    return render_template('index.html', attributes=attributes, prepopulated_values=prepopulated_values, result=result)

if __name__ == '__main__':
    app.run(debug=True)
