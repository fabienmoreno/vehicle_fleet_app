from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    # Listening on all interfaces is required in a containerized environment.
    app.run(host='0.0.0.0', port=5000)
