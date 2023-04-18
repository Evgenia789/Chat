import logging
import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename='main.log',
    filemode='w'
)

connected_clients = set()

def handle_client(conn: socket.socket, address: tuple) -> None:
    logging.info("New client connected: %s", address)
    connected_clients.add(conn)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            logging.info("Received from client %s: %s", address, data)
            for client in connected_clients:
                if client != conn:
                    client.sendall(data)
    logging.info("Client %s disconnected", address)
    connected_clients.remove(conn)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    logging.info("Server listening on %s:%s", HOST, PORT)
    while True:
        conn, address = s.accept()
        logging.info("New connection from %s", address)
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, address)
        ).start()
