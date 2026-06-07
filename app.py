from flask import Flask, render_template, request, jsonify
import FFVIII_CardGame_AI as ai
import yaml
import os

app = Flask(__name__)

# Global game state for simplicity in a local tool
current_gs = None

def gs_to_dict(gs):
    if gs is None:
        return None
    
    board = {}
    for pos, card in gs.board.items():
        if card:
            board[pos] = {
                "symbol": card.symbol,
                "owner": card.owner,
                "top": card.top,
                "left": card.left,
                "right": card.right,
                "bottom": card.bottom
            }
        else:
            board[pos] = None
            
    hands = {
        ai.PLAYER: [],
        ai.OPPONENT: []
    }
    for p in [ai.PLAYER, ai.OPPONENT]:
        for symbol, card in gs.players[p].hand.items():
            hands[p].append({
                "symbol": card.symbol,
                "owner": card.owner,
                "top": card.top,
                "left": card.left,
                "right": card.right,
                "bottom": card.bottom
            })
            
    return {
        "board": board,
        "hands": hands,
        "current_player": gs.current_player,
        "points": gs.points,
        "game_over": gs.game_over()
    }

@app.route('/')
def index():
    return render_template('index.html')
# History management
history_stack = []
redo_stack = []

def save_state():
    global current_gs, history_stack, redo_stack
    if current_gs:
        history_stack.append(current_gs.clone())
        # Clear redo stack whenever a new move is made
        redo_stack = []

@app.route('/api/init', methods=['POST'])
def init_game():
    global current_gs, history_stack, redo_stack
    data = request.json

    if data.get('load_default'):
        current_gs = ai.gamestate_from_file('gamestate.yaml')
    else:
        # Custom initialization from setup form
        current_gs = ai.GameState()
        current_gs.current_player = data['current_player']

        for card_data in data['cards']:
            card = ai.Card(
                symbol=card_data['symbol'],
                owner=card_data['owner'],
                top=int(card_data['top']),
                left=int(card_data['left']),
                right=int(card_data['right']),
                bottom=int(card_data['bottom'])
            )
            current_gs.players[card_data['owner']].hand[card_data['symbol']] = card

    # Initialize stacks
    history_stack = []
    redo_stack = []

    return jsonify(gs_to_dict(current_gs))

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(gs_to_dict(current_gs))

@app.route('/api/move', methods=['POST'])
def make_move():
    global current_gs
    data = request.json
    card_symbol = data['symbol']
    position = int(data['position'])

    if current_gs:
        save_state()
        current_gs.make_move(card_symbol, position)

    return jsonify(gs_to_dict(current_gs))

@app.route('/api/undo', methods=['POST'])
def undo_move():
    global current_gs, history_stack, redo_stack
    if history_stack:
        redo_stack.append(current_gs.clone())
        current_gs = history_stack.pop()
    return jsonify(gs_to_dict(current_gs))

@app.route('/api/redo', methods=['POST'])
def redo_move():
    global current_gs, history_stack, redo_stack
    if redo_stack:
        history_stack.append(current_gs.clone())
        current_gs = redo_stack.pop()
    return jsonify(gs_to_dict(current_gs))

@app.route('/api/recommend', methods=['GET'])
def recommend_move():
    global current_gs
    if current_gs and not current_gs.game_over():
        depth = int(request.args.get('depth', 4))
        
        # Get evaluations for all moves
        all_move_evals = []
        best_m = None
        best_s = -float('inf')
        
        for move in current_gs.next_possible_moves():
            card_symbol, position = move
            new_gs = current_gs.clone()
            new_gs.make_move(card_symbol, position)
            
            # Opponent will play optimally, so we use minimax starting from their turn
            score = ai.minimax(
                new_gs, False, 1, depth, current_gs.current_player, -ai.math.inf, ai.math.inf
            )
            
            all_move_evals.append({
                "symbol": card_symbol,
                "position": position,
                "score": score
            })
            
            if score > best_s:
                best_s = score
                best_m = move
        
        # Sort all moves by score (highest first)
        all_move_evals.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            "move": {
                "symbol": best_m[0],
                "position": best_m[1]
            },
            "score": best_s,
            "all_evals": all_move_evals,
            "depth": depth
        })
    return jsonify({"error": "Game not started or already over"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
