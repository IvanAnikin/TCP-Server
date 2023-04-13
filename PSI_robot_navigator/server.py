import socket
import threading
import select
import random

from enums import *
from communication_standard import *

def receive_packet(conn):
    packet = b""
    while True:
        ready_to_read, _, _ = select.select([conn], [], [], 1)
        if not ready_to_read: return False
        
        chunk = conn.recv(1024) 
        if not chunk:
            raise ConnectionError("Connection closed by remote host")
        packet += chunk
        if packet.endswith(b"\a\b"):
            break
    return packet.decode('ascii')

def handle_client(conn, addr):
    print(f"New connection from {addr[0]}:{addr[1]}")

    connection_status = Connection_status.BEFORE_USERNAME
    username = ""
    hash_code = 0
    pos_x       = 0
    pos_y       = 0
    prev_x      = 0
    prev_y      = 0
    dir         = 0     #   [ 0: N | 1: E | 2: N | 3: W ]
    prev_dir    = 0     #   [ 0: N | 1: E | 2: N | 3: W ]
    dir_check = True

    breakbreak = False

    while True:
        '''
        ready_to_read, _, _ = select.select([conn], [], [], 1)
        if not ready_to_read: break
        '''
        data_pack = receive_packet(conn)
        if not data_pack: break
        if isinstance(data_pack, bool): break

        print("Data received: ")
        print(data_pack)
        
        messages = data_pack.split("\a\b")
        data_array = [messages[i] + "\a\b" for i in range(len(messages) - 1)] + [messages[-1]]
        data_array.pop()

        print("data array:")
        print(data_array)

        for data in data_array:
            same_pos = False
            
            print("data inside the array:")
            print(data)

            data_state = check_data(data)
            if data_state != Response_status.SUCCESS:
                print("syntax error")
                conn.send("301 SYNTAX ERROR\a\b".encode('ascii'))
                breakbreak = True
                break

            data = data[0:len(data)-2]

            if(connection_status == Connection_status.BEFORE_USERNAME):
                username = data
                conn.send("107 KEY REQUEST\a\b".encode('ascii'))
                connection_status = Connection_status.KEY_REQUEST_SENT

            elif(connection_status == Connection_status.KEY_REQUEST_SENT):
                
                if not data.isnumeric():
                    conn.send("301 SYNTAX ERROR\a\b".encode('ascii'))
                    print("Synt. error 1")
                    breakbreak = True
                    break

                print("converting this to int:")
                print(data)
                if(int(data) not in range(5)):
                    conn.send("303 KEY OUT OF RANGE\a\b".encode('ascii'))
                    breakbreak = True
                    break
                
                key_found = False
                id = 0
                for code in codes:
                    if(code[0] == codes[int(data)][0]):
                        
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
                    breakbreak = True
                    break
            
            elif (connection_status == Connection_status.KEY_SHARED):
                
                # check hash
                print("*\t The client shared his hash code and I'm gonna check it now and confirm or feject the connection\n");

                print("Converting to int:")
                print(data)
                received_hash = int(data)

                hash_code = 0
                for symbol in username:
                    hash_code += ord(symbol)

                print("ascii sum = " + str(hash_code))
                hash_code *= 1000
                hash_code %= 65536
                print("hash1 = " + str(hash_code))
                hash_code += int(code[1])
                hash_code %= 65536
                print("hash2 = " + str(hash_code))

                print("received_hash = " + str(received_hash))

                #if(codes[int(response[0:len(response)-2])][1] != code[1]):
                if received_hash != hash_code:
                    conn.send("300 LOGIN FAILED\a\b".encode('ascii'))

                    response_status = Connection_status.LOGIN_FAILED
                    response_status.show()
                    breakbreak = True
                    break
                
                conn.send("200 OK\a\b".encode('ascii'))
                conn.send("102 MOVE\a\b".encode('ascii'))
                connection_status = Connection_status.LOGGED_IN

            elif(connection_status == Connection_status.LOGGED_IN):
                print("LOGGED_IN")
                data = str(data)
                prev_x = pos_x
                prev_y = pos_y
                try:
                    state, pos_x, pos_y = extract_data_from_string(data, pos_x, pos_y)
                except ValueError:
                    conn.send("301 SYNTAX ERROR\a\b\a\b".encode('ascii'))
                    print("Synt. error 2")
                    breakbreak = True
                    break
                print("state = " + str(state))
                if(state == 0):
                    print("x: " + str(pos_x) + " y: " + str(pos_y) + " dir: " + str(dir))

                if(pos_x == 0 and pos_y == 0):
                    print("Got to 0,0 | asking for message")
                    conn.send("105 GET MESSAGE\a\b".encode('ascii'))
                    connection_status = Connection_status.AWAITING_MESSAGE
                    print("switched to AWAITING_MESSAGE 2")
                    continue
                    
                conn.send("102 MOVE\a\b".encode('ascii'))
                connection_status = Connection_status.POSITION_KNOWN
                print("switched to POSITION_KNOWN")
                continue
                
            elif(connection_status == Connection_status.POSITION_KNOWN):
                
                
                data = str(data)
                prev_x = pos_x
                prev_y = pos_y
                prev_dir = dir
                
                try:
                    state, pos_x, pos_y = extract_data_from_string(data, pos_x, pos_y)
                except ValueError:
                    conn.send("301 SYNTAX ERROR\a\b\a\b".encode('ascii'))
                    print("Synt. error 3")
                    breakbreak = True
                    break
                    
                
                if(state == 0):
                    
                    if(dir_check):
                        if(prev_x - pos_x == -1):
                            dir = 1
                        elif(prev_x - pos_x == 1):
                            dir = 3
                        elif(prev_y - pos_y == -1):
                            dir = 0
                        elif(prev_y - pos_y == 1):
                            dir = 2
                        dir_check = False

                    print("x: " + str(pos_x) + " y: " + str(pos_y) + " dir: " + str(dir))

                    move = 0    # 0 = move | 1 = left | 2 = right

                    if(pos_x == 0 and pos_y == 0):
                        print("Got to 0,0 | asking for message")
                        conn.send("105 GET MESSAGE\a\b".encode('ascii'))
                        print("switched to AWAITING_MESSAGE")
                        connection_status = Connection_status.AWAITING_MESSAGE
                        continue
                    elif(pos_x < 0):
                        if(dir == 0): move = 2 
                        if(dir == 1): move = 0 
                        if(dir == 2): move = 1 
                        if(dir == 3): move = 1 
                    elif(pos_x > 0):
                        if(dir == 0): move = 1
                        if(dir == 1): move = 1
                        if(dir == 2): move = 2
                        if(dir == 3): move = 0
                    elif(pos_y < 0):
                        if(dir == 0): move = 0
                        if(dir == 1): move = 1
                        if(dir == 2): move = 1
                        if(dir == 3): move = 2
                    elif(pos_y > 0):
                        if(dir == 0): move = 1
                        if(dir == 1): move = 2
                        if(dir == 2): move = 0
                        if(dir == 3): move = 1
                    else:
                        conn.send("301 SYNTAX ERROR\a\b".encode('ascii'))
                        print("Synt. error 4")
                        breakbreak = True
                        break    
                    
                    if(prev_x == pos_x and prev_y == pos_y): 
                        same_pos = True
                        move = random.randint(0, 2)
                        print("same_pos = True")
                    
                    print("move: " + str(move))

                    if(move == 0):      conn.send("102 MOVE\a\b".encode('ascii'))
                    elif(move == 1):
                        dir -= 1
                        if(dir<0): dir = 3
                        conn.send("103 TURN LEFT\a\b".encode('ascii'))
                    else:
                        dir += 1
                        if(dir >= 4): dir = 0
                        conn.send("104 TURN RIGHT\a\b".encode('ascii'))

                elif state == 1:
                    print("recharging")
                    if(charging):
                        conn.send("302 LOGIC ERROR\a\b".encode('ascii'))
                        breakbreak = True
                        break
                    charging = True
                elif state == 2:
                    print("recharged")
                    if not charging: 
                        conn.send("302 LOGIC ERROR\a\b".encode('ascii'))
                        breakbreak = True
                        break
                    charging = False
                
            elif(connection_status == Connection_status.AWAITING_MESSAGE):
                print("AWAITING_MESSAGE condition")
                conn.send("106 LOGOUT\a\b".encode('ascii'))
                breakbreak = True
                break
            else:
                print("wrong state")
                breakbreak = True
                break

        if(breakbreak): break
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
