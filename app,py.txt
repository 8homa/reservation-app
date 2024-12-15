from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 予約データ（メモリ上に保持）
reservations = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reservations', methods=['GET', 'POST'])
def handle_reservations():
    global reservations
    if request.method == 'POST':
        data = request.json
        date = data.get('date')
        time = data.get('time')
        user = data.get('user')

        if not date or not time or not user:
            return jsonify({'error': 'Invalid data'}), 400

        if date not in reservations:
            reservations[date] = {}

        if time in reservations[date]:
            return jsonify({'error': 'Time slot already reserved'}), 409

        reservations[date][time] = user
        return jsonify({'message': 'Reservation successful'}), 201

    return jsonify(reservations)
