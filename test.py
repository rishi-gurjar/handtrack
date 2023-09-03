from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import random
import threading 
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
    sid = request.sid  # Get the Session ID of the current client
    socketio.start_background_task(background_task, sid)

def background_task(sid):
    numbers = list(range(1, 11))
    def emit_number():
        random_number = random.choice(numbers)
        print('Emitting new number:', random_number)
        socketio.emit('server event', {'data': random_number}, room=sid)
        threading.Timer(1, emit_number).start()
    emit_number()

"""
    while True:
        random_number = random.choice(numbers)
        print('Emitting new number:', random_number)
        socketio.emit('server event', {'data': random_number}, room=sid)  # Use the sid as room
        Timer(1, background_task, args=(sid,)).start()
        #time.sleep(1)
"""
if __name__ == '__main__':
    print("About to run the app.")
    try:
        socketio.run(app, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")

## RUN: python3 test.py