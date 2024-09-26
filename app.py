from flask import Flask, request, send_file, jsonify
import requests
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/")
def home():
    return jsonify({"message": "hello world"})

@app.route('/fetch-image', methods=['GET'])
def fetch_image():

    session = requests.Session()

    image_url = request.args.get('url')
   
    if not image_url:
        return jsonify({"error": "No URL provided"}), 400
    
    first_response = session.get(image_url)
    first_headers = first_response.headers["content-type"]
    if first_headers == "image/jpeg":
        return send_file(BytesIO(first_response.content), mimetype='image/jpeg')
    else:
        second_response = session.get(image_url)
        print("second response:")
        second_headers = second_response.headers["content-type"]
        if second_headers == "image/jpeg":

            return send_file(BytesIO(second_response.content), mimetype='image/jpeg')
        else:
            return jsonify({"error": "Not Found"}), 404


if __name__ == '__main__':
    app.run(debug=True)