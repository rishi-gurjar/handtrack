
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = 69
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Note the port number


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