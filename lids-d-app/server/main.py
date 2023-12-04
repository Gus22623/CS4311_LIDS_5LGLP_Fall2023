from flask import Flask
from flask_cors import CORS
import routes
import socket
import threading
from cryptography.fernet import Fernet
from db import cursor, db

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

    client_key = b'u-Tab2rqhRSPz5IO4yz_qy3fGtAQr-ohHahuPXSsidg='
    print("KEY IS:", client_key)
    
    while True:
        client_socket, address = server.accept()
        print("Accepted connection from ", address)
           
        # Handle the connection in a seperate thread
        client_handler =threading.Thread(target=handle_client, args=(client_socket,client_key), daemon=True)
        client_handler.start()
        
def handle_client(client_socket,key):
    print("Client Connected")
    
    cipher_suite = Fernet(key)
    
    try:
        while True:
            # Receive data from the client
            encrypted_data = client_socket.recv(1024)
            
            if not encrypted_data:
                # If no data is received the clign might have disconnected
                print("Client Disconnected")
                break
            
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            
            # Process the received data
            process_received_data(decrypted_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error handling client: {e}")
    finally:
        # Close the client socket when the loop breaks
        client_socket.close()

def process_received_data(data):
    received_alert = data.decode('utf-8').split(',')
    print(f"Received alert: {received_alert}")
    
    try:
            # Execute SQL query to insert the alert data into the 'alert' table
            sql_insert_alert = (
                "INSERT INTO alert (level, time, source_ip, dest_ip, src_port, dest_port, protocol, description) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )

            cursor.execute(sql_insert_alert, (
                received_alert[0],
                received_alert[1],
                received_alert[2],
                received_alert[3],
                received_alert[4],
                received_alert[5],
                received_alert[6],
                received_alert[7]    
            ))

            db.commit()
            print("Alert stored in the database.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Alert not stored in the database.")
        db.rollback()
    
    
if __name__ == '__main__':
    # Start the socket server in a seperate thread
    socket_thread = threading.Thread(target=socket_server, daemon=True)
    socket_thread.start()
    
    # Start the Flask app
    app.run(debug=True, port=5000)


