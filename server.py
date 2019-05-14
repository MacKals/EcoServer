
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def handleData():
	if request.method == 'POST':
		jsonData = request.get_json()
		print(jsonData['payload_fields']['data'])
		return '...'
	return "Running and ready"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5200)
