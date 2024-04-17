import socket
import os
import time
import shutil
import tenseal as ts
import utils
from deepface import DeepFace

def encrypt(folder_path):
    # try:
    #     os.makedirs("Encrypted_images")
    # except FileExistsError:
    #     shutil.rmtree("Encrypted_images")
    #     os.makedirs("Enrypted_images")
    #     pass

    context = ts.context_from(utils.read_data("D:\Major project\Virtual environment\Project\Edge\keys\secret.txt"))

    for i in os.listdir(folder_path):
        try:
            image_embedding = DeepFace.represent(os.path.join(folder_path,i),model_name="Facenet")[0]['embedding']
        except ValueError:
            continue
        encrypted = ts.ckks_vector(context,image_embedding)
        utils.write_data(f"Encrypted_images/{i[:-4]}.txt",encrypted.serialize())
    print("All files encrypted")
    return

def receive_files(server_socket, folder_path):
    conn, addr = server_socket.accept()
    print("Connection established with", addr)
    
    s = time.time()

    while True:
        filename = conn.recv(1024).decode()
        if filename == "End":
            print("All files received")
            #encrypt(folder_path)
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
    
    if not os.path.exists("Encrypted_images"):
        os.makedirs("Encrypted_images")
    
    receive_files(server_socket, folder_path)

if __name__ == "__main__":
    main()