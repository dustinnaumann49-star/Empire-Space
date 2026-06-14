from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

SAVES_DIR = "saves"
os.makedirs(SAVES_DIR, exist_ok=True)

@app.route('/save', methods=['POST'])
def save_game():
    data = request.json
    player_name = data.get('player_name', 'default')
    game_state = data.get('game_state', {})
    
    with open(f'{SAVES_DIR}/{player_name}.json', 'w') as f:
        json.dump(game_state, f)
    
    return jsonify({"status": "ok", "player": player_name})

@app.route('/load/<player_name>', methods=['GET'])
def load_game(player_name):
    try:
        with open(f'{SAVES_DIR}/{player_name}.json', 'r') as f:
            game_state = json.load(f)
        return jsonify(game_state)
    except:
        return jsonify({"error": "No save found"}), 404

@app.route('/players', methods=['GET'])
def get_players():
    players = []
    if os.path.exists(SAVES_DIR):
        for file in os.listdir(SAVES_DIR):
            if file.endswith('.json'):
                players.append(file.replace('.json', ''))
    return jsonify(players)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
