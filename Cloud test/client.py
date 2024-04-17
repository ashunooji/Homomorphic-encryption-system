import socket
import os

def send_photos(client_socket):
    folder_path = "Server photos"
    files = os.listdir(folder_path)
    for file_name in files[:20]:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rb') as file:
            file_size = os.path.getsize(file_path)
            # Send file name, size, and data
            client_socket.sendall(file_name.encode())
            client_socket.recv(1024)  # Wait for ACK
            client_socket.sendall(str(file_size).encode())
            client_socket.recv(1024)  # Wait for ACK
            
            # Send file data in chunks
            with open(file_path, 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    if not file_data:
                        break
                    client_socket.sendall(file_data)
                print(f"File '{file_name}' sent")
                client_socket.recv(1024)  # Wait for ACK
            
    # Signal end of file transfer
    client_socket.sendall(b"End")
    print("All files sent")
    t = client_socket.recv(1024).decode()
    print(f"Time taken to transfer is {t} seconds")

def main():
    #host = "172.173.248.90"
    host = "127.0.0.1"
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    send_photos(client_socket)
    client_socket.close()

if __name__ == "__main__":
    main()
