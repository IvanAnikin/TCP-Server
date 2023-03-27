import socket
import random 
import time

from enums import *
from communication_standard import *


def send_message(client_socket, message):
    client_socket.send(message.encode())

def get_response():
    response = client_socket.recv(1024).decode()

    print(f"Server response: {response}")
    response_status = check_data(response)
    response_status.show()

    return response, response_status

if __name__ == "__main__":

    host = "localhost"
    port = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_status = Client_status.BEFORE_USERNAME
    response = ""
    response_status = Response_status.SUCCESS

    robot_dir =  random.randint(0, 4)
    position_x = random.randint(0, 5)
    position_y = random.randint(0, 5)
    prev_x = position_x
    prev_y = position_y
    prev_dir = robot_dir


    #if client_status == Client_status.BEFORE_USERNAME:
    username = "Mnau!" 
    message = username
    client_status = Client_status.USERNAME_SENT
    message += "\a\b"
    send_message(client_socket, message)

    while True:

        response, response_status = get_response()

        if ( response_status != Response_status.SUCCESS):
            break

        elif client_status == Client_status.USERNAME_SENT:
            random_int = random.randint(0, 4)
            code = codes[random_int]
            message = str(random_int)
            client_status = Client_status.KEY_SENT

        elif client_status == Client_status.KEY_SENT:

            received_hash = int(response[0:len(response)-2])

            hash_code = 0
            for symbol in username:
                hash_code += ord(symbol)
            print("ascii sum = " + str(hash_code))
            hash_code *= 1000
            hash_code %= 65536
            print("hash1 = " + str(hash_code))
            hash_code += int(code[0])
            hash_code %= 65536
            print("hash2 = " + str(hash_code))

            print("received_hash = " + str(received_hash))

            #if(codes[int(response[0:len(response)-2])][1] != code[1]):
            if received_hash != hash_code:
                response_status = Response_status.WRONG_CODE
                response_status.show()
                break

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

            message = str(hash_code)

            client_status = Client_status.HASH_SENT

        elif client_status == Client_status.HASH_SENT:

            if(response == "200 OK\a\b"):
                client_status = Client_status.KEY_APPROVED
            
            else:
                print("Login failed")
                break

        elif client_status == Client_status.KEY_APPROVED:
            #print("**")

            if response == "102 MOVE\a\b":
                prev_dir = robot_dir
                if(dir == 0 or dir == 2):
                    prev_y = position_y
                    if(dir == 0):
                        position_y += 1
                    else:
                        position_y -= 1
                if(dir == 1 or dir == 3):
                    prev_x = position_x
                    if(dir == 1):
                        position_x += 1
                    else:
                        position_y -= 1

            elif response == "103 TURN LEFT\a\b":
                prev_dir = robot_dir
                robot_dir -= 1
                if robot_dir < 0:
                    robot_dir = 4 - robot_dir

            elif response == "104 TURN RIGHT\a\b":
                prev_dir = robot_dir
                robot_dir += 1
                if robot_dir < 0:
                    robot_dir = 4 - robot_dir
            else:
                print("Strange response")
                time.sleep(5)
            #message = input()

            message = "OK" + str(position_x) + " " + str(position_y)
            
        # if client_status == Client_status.KEY_APPROVED: continue

        message += "\a\b"
        send_message(client_socket, message)

    client_socket.close()

