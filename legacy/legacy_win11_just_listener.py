import socket
import threading

# System configuration
IP = '192.168.1.105'
PORT = 6769

# Start server, listen for connections
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    # Accept connection and start client handler thread
    while True:
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# Receive data from connection
def handle_client(client_socket):
    with client_socket as sock:
        while True:
            request = sock.recv(1024)
            print(f'[*] Received: {request.decode("utf-8")}')
            sock.send(b'ACK')

if __name__ == '__main__':
    main()