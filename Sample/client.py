import socket

def send_message(message):
    host = "localhost"
    port = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(message.encode())
    response = client_socket.recv(1024)
    client_socket.close()
    return response.decode()

if __name__ == "__main__":
    message = "Hello, server!"
    response = send_message(message)
    print(f"Server response: {response}")