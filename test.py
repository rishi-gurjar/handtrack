from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    print('Rendered webpage')
    return render_template('test.html')

@socketio.on('my event')
def handle_my_event(message):
    print('Received:', message['data'])
    numbers = list(range(1, 11))
   # for n in range(1, 11):
    random_number = random.choice(numbers)
    print('Emitting new number: ', random_number)
    emit('server event', {'data': random_number})
     #   time.sleep(1)

"""
    numbers = list(range(1, 11))
    while True:
        random_number = random.choice(numbers)
        print('Emitting new number: ', random_number)
        emit('server event', {'data': random_number})
        time.sleep(1)
"""

if __name__ == '__main__':
    print("About to run the app.")
    try:
        socketio.run(app, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")

## RUN: python3 test.py