import socket
import os
import time

def receive_files(server_socket, folder_path):
    conn, addr = server_socket.accept()
    print("Connection established with", addr)
    
    s = time.time()

    while True:
        filename = conn.recv(1024).decode()
        if filename == "End":
            print("All files received")
            e = time.time()
            t = str(e-s)
            conn.sendall(t.encode())
            break
        
        # Send ACK to signal readiness for file name
        conn.sendall(b"ACK")
        
        # Receive file size and send ACK
        file_size = int(conn.recv(1024).decode())
        conn.sendall(b"ACK")
        
        # Receive file data in chunks
        received_data = b""
        while len(received_data) < file_size:
            data_chunk = conn.recv(1024)
            if not data_chunk:
                break
            received_data += data_chunk
        
        # Write received data to file
        with open(os.path.join(folder_path, filename), 'wb') as file:
            file.write(received_data)
        
        # Send ACK to signal successful file reception
        conn.sendall(b"ACK")
        print(f"Received file '{filename}'")

def main():
    host = "0.0.0.0"
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")

    folder_path = "Received_photos"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    receive_files(server_socket, folder_path)

if __name__ == "__main__":
    main()