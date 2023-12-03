from flask import Flask
from flask_cors import CORS
import routes
import socket
import threading
from cryptography.fernet import Fernet

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

@app.route('/getAlertsProtocol', methods=['GET'])
def get_alerts_protocol():
    return routes.get_alerts_protocol()

@app.route('/filterLevel_1', methods=['GET'])
def filter_level_1():
    return routes.filter_level_1()

@app.route('/filterLevel_2', methods=['GET'])
def filter_level_2():
    return routes.filter_level_2()

@app.route('/filterLevel_3', methods=['GET'])
def filter_level_3():
    return routes.filter_level_3()

def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(('127.0.0.1', 5010))
    server.listen(5)
    
    print("Socket server listening on port 5010...")
    
    while True:
        client_socket, address = server.accept()
        print("Accepted connection from ", address)
        
        # Handle the connection in a seperate thread
        client_handler =threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
        client_handler.start()
        
def handle_client(client_socket):
    print("Client Connected")
    
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            
            if not data:
                # If no data is received the clign might have disconnected
                print("Client Disconnected")
                break
            
            # Process the received data
            process_received_data(data)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Close the client socket when the loop breaks
        client_socket.close()

def process_received_data(data):
    print(f"Processing data: {data}")
    received_alert = data.decode('utf-8').split(',')
    print(f"Received alert: {received_alert}")
    
if __name__ == '__main__':
    # Start the socket server in a seperate thread
    socket_thread = threading.Thread(target=socket_server, daemon=True)
    socket_thread.start()
    
    # Start the Flask app
    app.run(debug=True, port=5000)


