from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "dsfsdf!"

@app.route('/get', methods=['GET'])
def get_method():
    data = {
        "message": "Hadfgsdfg"
    }
    return jsonify(data)

@app.route('/post', methods=['POST'])
def post_method():
    received_data = request.json
    response_data = {
        "message": "adfgadfg",
        "received_data": received_data
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
