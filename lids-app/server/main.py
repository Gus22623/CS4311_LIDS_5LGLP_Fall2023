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

@app.route('/getAlertsLevel', methods=['GET'])
def get_alerts_level():
    return routes.get_alerts_level()

@app.route('/getAlertsTime', methods=['GET'])
def get_alerts_time():
    return routes.get_alerts_time()

@app.route('/getAlertsIP', methods=['GET'])
def get_alerts_ip():
    return routes.get_alerts_ip()

@app.route('/filterLevel_1', methods=['GET'])
def filter_level_1():
    return routes.filter_level_1()

@app.route('/filterLevel_2', methods=['GET'])
def filter_level_2():
    return routes.filter_level_2()

@app.route('/filterLevel_3', methods=['GET'])
def filter_level_3():
    return routes.filter_level_3()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


