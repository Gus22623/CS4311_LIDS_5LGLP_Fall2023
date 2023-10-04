from flask import Flask
from flask_cors import CORS
import routes

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/upload-xml', methods=['POST'])
def handle_upload():
    return routes.upload_xml()

@app.route('/getAlerts', methods=['GET'])
def get_alerts():
    return routes.getAlerts()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
