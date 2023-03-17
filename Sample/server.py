import socket
import threading

def handle_client(conn, addr):
    print(f"New connection from {addr[0]}:{addr[1]}")
    data = conn.recv(1024)
    response = b"Hello, client!"
    conn.send(response)
    conn.close()

def start_server():
    host = "0.0.0.0"
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
