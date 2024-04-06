import socket

# Server configuration
SERVER_IP = '172.173.248.90'  # Replace x.x.x.x with the server's public IP address
SERVER_PORT = 53  # Server's port number

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Send a message to the server
message = "hi"
client_socket.sendall(message.encode())

# Receive response from the server
response = client_socket.recv(1024)
print("Response from server:", response.decode())

# Close the connection
client_socket.close()
