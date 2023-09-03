from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

@app.route('/')
def index():
    print('Rendered webpage')
    return render_template('index.html')

@socketio.on('connect')
def handle_connection():
    print("Client connected")
    numbers = list(range(1, 11))
    while True:
        random_number = random.choice(numbers)
        print('Emitting new number: ', random_number)
        socketio.emit('new_number', {'number': random_number})
        time.sleep(1)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)


"""
from flask import Flask, render_template, jsonify
from script import run_script  # Import the function from script.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

square_colors = {'square_1': '#ffffff'}

@app.route('/change/<color>', methods=['GET'])
def change_color(color):
    print("POST GET COLOR:", color)
    square_colors['square_1'] = f"#{color}"
    return jsonify({'color': square_colors['square_1']})

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Note the port number

    """