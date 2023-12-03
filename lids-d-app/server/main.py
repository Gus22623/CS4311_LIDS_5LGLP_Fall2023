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
    #server.close()
    server.bind(('127.0.0.1',5010))
    server.listen(5)

    print("SOCKET LISTENING ON port 5010...")

    while(True):
        client_socket, address = server.accept()
        print("Accepted connection from ", address)

        #handle connection in seperate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
        client_handler.start()

def handle_client(client_socket):
    print("Client connected")

    try:
        while True:
            #receive data from client
            data = client_socket.recv(1024)

            if not data:
                print("Client disconnected")
                break
            
            process_received_data(data)

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def process_received_data(data):
    print(f"Processing data: {data}")
    key = b'LidsTeam5Key1234567890123456'[:32]
    cipher_suite = Fernet(key)

    decrypted_data = cipher_suite.decrypt(encrypted_data)

    decrypted_data = data.decode('utf-8').split(',')
    print(f"Received alert: {decrypted_data}")

    try:
        sql_insert_alert = (
                "INSERT INTO alert (level, time, source_ip, dest_ip, src_port, dest_port, protocol, description) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )

        cursor.execute(sql_insert_alert, (
            decrypted_data[0], 
            decrypted_data[1],
            decrypted_data[2],
            decrypted_data[3],
            decrypted_data[4], 
            decrypted_data[5],
            decrypted_data[6],
            decrypted_data[7]
        ))

        db.commit()
    except Exception as e:
        print(f"Error storing alert from LIDS in database {str(e)}")

if __name__ == '__main__':
    #Start socket in seperate thread
    socket_thread = threading.Thread(target=socket_server, daemon=True)
    socket_thread.start()

    app.run(debug=True, port=5000)


