import socket
import os

def send_photos(conn):
    folder_path = "Server photos"
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rb') as file:
            file_size = os.path.getsize(file_path)
            # Send file name, size, and data
            conn.sendall(file_name.encode())
            conn.recv(1024)  # Wait for ACK
            conn.sendall(str(file_size).encode())
            conn.recv(1024)  # Wait for ACK
            
            # Send file data in chunks
            with open(file_path, 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    if not file_data:
                        break
                    conn.sendall(file_data)
                print(f"File '{file_name}' sent")
                conn.recv(1024)  # Wait for ACK
            
    # Signal end of file transfer
    conn.sendall(b"End")
    print("All files sent")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print("Connection established with", addr)
        try:
            send_photos(conn)
        finally:
            conn.close()
            break
