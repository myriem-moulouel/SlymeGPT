import socket
from slyme import SlymeDriver
import time




def chat_with_gpt3(user_message):
    # Make a request to the GPT-3 API
    slyme = SlymeDriver(pfname="Default")
    time.sleep(5)
    slyme.select_latest_chat()
    time.sleep(5)



    response = slyme.completion(user_message)
    time.sleep(5)

    slyme.end_session()
    return response




def start_server():
    host = '127.0.0.1'  # Server IP address
    port = 12345       # Port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server listening on {}:{}".format(host, port))

    while True:
        conn, addr = server_socket.accept()
        print("Connected to client at {}:{}".format(addr[0], addr[1]))

        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received message from client: {}".format(data))
            
            response = chat_with_gpt3(data)

            # Echo the message back to the client
            conn.sendall(response.encode('utf-8'))

        print("Connection closed with client at {}:{}".format(addr[0], addr[1]))
        conn.close()

if __name__ == "__main__":
    start_server()

