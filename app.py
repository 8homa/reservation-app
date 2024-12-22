import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# メモリ上で予約情報を管理する簡易実装
reservations = []

@app.route("/")
def index():
    return "Welcome to the Reservation System!"

@app.route("/init", methods=["GET"])
def init_reservations():
    """
    GET /init
    予約データを初期化
    """
    global reservations
    reservations = []
    return "Reservations initialized", 200

@app.route("/reserve", methods=["POST"])
def reserve():
    """
    POST /reserve
    JSON例:
    {
      "user_id": 1,
      "date": "2024-12-25",
      "time": "10:00"
    }
    同じ user_id, date, time が既にあれば重複エラー
    """
    data = request.get_json()
    if not data or "user_id" not in data or "date" not in data or "time" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # 重複チェック
    for r in reservations:
        if r["user_id"] == data["user_id"] and r["date"] == data["date"] and r["time"] == data["time"]:
            return jsonify({"error": "Already reserved"}), 409

    reservations.append({
        "user_id": data["user_id"],
        "date": data["date"],
        "time": data["time"]
    })
    return jsonify({"message": "Reservation created"}), 201

@app.route("/reservations", methods=["GET"])
def get_reservations():
    """
    GET /reservations
    登録済みの予約一覧を返す
    """
    return jsonify(reservations), 200

if __name__ == "__main__":
    # ローカル実行用 (本番では gunicornを使用する場合あり)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
