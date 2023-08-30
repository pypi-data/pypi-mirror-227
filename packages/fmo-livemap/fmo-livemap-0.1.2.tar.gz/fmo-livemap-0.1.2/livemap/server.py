from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/polylines", methods=["POST"])
def post_polyline():
    data = request.json

    socketio.emit("polyline", data)

    return jsonify({
        "id": data.get("name"),
        "name": data.get("name"),
        "points": []
    })

@app.route("/polylines/<id>/points", methods=["POST"])
def post_path_point(id):
    data = request.json
    data["name"] = id
    if isinstance(data, list):
        for data_point in data:
            socketio.emit("pathPoint", data_point)
    else:
        socketio.emit("pathPoint", data)

    return data, 200

def run_server(port, debug=False):
    socketio.run(app, port=port, debug=debug)

if __name__ == '__main__':
    run_server(port=5050, debug=True)