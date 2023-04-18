import socket
import threading
import logging

HOST = "127.0.0.1"
PORT = 12345

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename='main.log',
    filemode='w'
)

def send_message(s: socket.socket, name: str) -> None:
    while True:
        message = input()
        if message == "/exit":
            s.sendall(f"{name} has left the chat".encode())
            break
        s.sendall(f"{name}: {message}".encode())

def receive_messages(s: socket.socket) -> None:
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    logging.info("Connected to server")

    name = input("Enter your name: ").strip()
    while not name:
        name = input("Your name must not be empty: ").strip()

    s.sendall(name.encode())

    send_thread = threading.Thread(target=send_message, args=(s, name))
    send_thread.start()

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    logging.info("Disconnected from server")
