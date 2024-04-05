import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345  # Port to listen on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(1)

print("Server listening on port", PORT)

# Accept a client connection
client_socket, client_address = server_socket.accept()

print("Connected to client:", client_address)

# Receive data from the client
data = client_socket.recv(1024)

print("Received:", data.decode())

# Send a response back to the client
client_socket.sendall("Hello from the server!".encode())

# Close the connection
client_socket.close()
server_socket.close()
