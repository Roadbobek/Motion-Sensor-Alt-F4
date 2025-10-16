import socket
import threading
from pynput.keyboard import Key, Controller
import time

# Initialize the keyboard controller
keyboard = Controller()

# System configuration
IP = '192.168.1.105'
PORT = 6769


def send_alt_f4():
    """Simulates the Alt+F4 key combination to close the active window."""
    # print("Sending Alt+F4 command...")
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.f4)
    keyboard.release(Key.alt)
    print("Alt+F4 command sent!")


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
    connection_start_time = time.time()
    time_limit_seconds = 10.0
    armed = False
    with client_socket as sock:
        sock.setblocking(False)  # Let loop run in background
        while True:
            time_elapsed = time.time() - connection_start_time
            if not armed and time_elapsed > time_limit_seconds:
                print(f"{time_limit_seconds} seconds have passed, ALt+F4 is now ARMED!")
                armed = True

            try:
                request = sock.recv(1024)
                if request:
                    data = request.decode("utf-8")
                    print(f'[*] Received: {data}')

                    if armed and data == "motion":
                        print("Received 'motion' signal. Triggering Alt+F4.")
                        send_alt_f4()
                        connection_start_time = time.time()
                        armed = False
                        print(f"Program disarmed for {time_limit_seconds} seconds.")

                    sock.send(b'ACK')
                else:
                    # Connection closed by client
                    break
            except BlockingIOError:
                # No data to read, continue loop
                pass

            time.sleep(0.1)  # Prevent busy waiting


if __name__ == '__main__':
    main()
