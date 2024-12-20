import socket
import threading

# Server details
HOST = '127.0.0.1'  # Localhost
PORT = 55555        # Arbitrary port

# List to hold clients and their corresponding usernames
clients = {}
addresses = {}

# Function to broadcast a message to all clients
def broadcast(message, client_socket):
    for client in clients:
        if clients[client] != clients[client_socket]:
            client.send(message)

# Function to send direct message to a specific client
def send_direct_message(message, target_username):
    for client, username in clients.items():
        if username == target_username:
            client.send(message.encode('utf-8'))

# Handle client messages
def handle_client(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = username
    broadcast(f"{username} has joined the chat!".encode('utf-8'), client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/dm"):  # Direct Message command
                # Extract target username and message
                split_message = message.split(' ', 2)
                if len(split_message) < 3:
                    client_socket.send("Invalid direct message format. Use /dm <username> <message>".encode('utf-8'))
                else:
                    target_username = split_message[1]
                    direct_message = split_message[2]
                    send_direct_message(f"{username} (direct): {direct_message}", target_username)
            else:
                broadcast(f"{username}: {message}".encode('utf-8'), client_socket)
        except:
            client_socket.close()
            del clients[client_socket]
            broadcast(f"{username} has left the chat.".encode('utf-8'), client_socket)
            break

# Main server function to handle incoming connections
def server_program():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server is running on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")

        client_socket.send("Enter your username:".encode('utf-8'))
        addresses[client_socket] = client_address

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    server_program()
