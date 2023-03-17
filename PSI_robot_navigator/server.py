import socket
import threading

from enums import *
from communication_standard import *


def handle_client(conn, addr):
    print(f"New connection from {addr[0]}:{addr[1]}")

    connection_status = Connection_status.BEFORE_USERNAME
    username = ""
    hash_code = 0

    while True:

        data = conn.recv(1024).decode('ascii')
        
        if not data:
            break

        print("Data received: ")
        print(data)

        data_state = check_data(data)
        if data_state == Response_status.SUCCESS:

            data = data[0:len(data)-2]

            if(connection_status == Connection_status.BEFORE_USERNAME):
                username = data
                conn.send("107 KEY REQUEST\a\b".encode('ascii'))
                connection_status = Connection_status.KEY_REQUEST_SENT

            elif(connection_status == Connection_status.KEY_REQUEST_SENT):
                
                if not data.isnumeric():
                    conn.send("301 SYNTAX ERROR\a\b".encode('ascii'))
                    break

                if(int(data) not in range(5)):
                    conn.send("303 KEY OUT OF RANGE\a\b".encode('ascii'))
                    break
                
                key_found = False
                id = 0
                for code in codes:
                    if(code[0] == codes[int(data)][0]):
                        #conn.send((str(id)+"\a\b").encode('ascii'))
                        
                        for symbol in username:
                            hash_code += ord(symbol)
                        print("ascii sum = " + str(hash_code))
                        hash_code *= 1000
                        hash_code %= 65536
                        print("hash1 = " + str(hash_code))
                        hash_code += int(code[0])
                        hash_code %= 65536
                        print("hash2 = " + str(hash_code))

                        conn.send((str(hash_code)+"\a\b").encode('ascii'))

                        connection_status = Connection_status.KEY_SHARED
                        key_found = True

                        break
                    id += 1
                if not key_found:
                    print("login failed")
                    conn.send("300 LOGIN FAILED\a\b".encode('ascii'))
                    break
            elif (connection_status == Connection_status.HASH_SHARED):
                
                # check hash
                print("*")

            elif(connection_status == Connection_status.KEY_SHARED):
                conn.send("102 MOVE\a\b".encode('ascii'))
                connection_status = Connection_status.KEY_SHARED_2

            elif(connection_status == Connection_status.KEY_SHARED_2):
                conn.send("102 MOVE\a\b".encode('ascii'))
                connection_status = Connection_status.POSITION_KNOWN

            elif(connection_status == Connection_status.POSITION_KNOWN):
                conn.send("103 TURN LEFT\a\b".encode('ascii'))
                sleep(5)
            else:
                print("wrong state")
                break

        else:
            print("syntax error")
            conn.send("301 SYNTAX ERROR\a\b".encode('ascii'))

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
