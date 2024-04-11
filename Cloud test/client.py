import socket
import os

def receive_files(client_socket, folder_path):
    while True:
        filename = client_socket.recv(1024).decode()
        if filename == "End":
            print("All files received")
            break
        
        # Send ACK to signal readiness for file name
        client_socket.sendall(b"ACK")
        
        # Receive file size and send ACK
        file_size = int(client_socket.recv(1024).decode())
        client_socket.sendall(b"ACK")
        
        # Receive file data in chunks
        received_data = b""
        while len(received_data) < file_size:
            data_chunk = client_socket.recv(1024)
            if not data_chunk:
                break
            received_data += data_chunk
        
        # Write received data to file
        with open(os.path.join(folder_path, filename), 'wb') as file:
            file.write(received_data)
        
        # Send ACK to signal successful file reception
        client_socket.sendall(b"ACK")
        print(f"Received file '{filename}'")

def main():
    host = "127.0.0.1"
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        folder_path = "Received_photos"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        receive_files(client_socket, folder_path)
    
    except Exception as e:
        print("Error:", e)
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
