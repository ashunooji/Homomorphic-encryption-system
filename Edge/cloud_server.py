import socket
import os
import pickle
from deepface import DeepFace
import tenseal as ts
import utils
import shutil


def search_res(res):
    result = []
    for keys,value in res.items():
        if value > -50 and value < 50:
            result.append(keys)
    return result


def decrypt_results():
    context = ts.context_from(utils.read_data('keys\secret.txt'))
    res = {}
    for i in os.listdir('Encrypted_results'):
        v = utils.read_data(os.path.join('Encrypted_results',i))
        v = ts.lazy_ckks_vector_from(v)
        v.link_context(context)
        res[i] = v.decrypt()[0]
    result = search_res(res)
    print("Results decrypted")
    print(res)
    return result


def send_files(client_socket, folder_path,public_key_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as file:
            client_socket.send(filename.encode())
            client_socket.recv(1024)  

            file_data = file.read(1024)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(1024)

            client_socket.send(b'DONE')
            client_socket.recv(1024)  
    print("Encrypted images files sent successfully")
    with open(public_key_path,'rb') as file:
        client_socket.send('public.txt'.encode())
        client_socket.recv(1024)
        file_data = file.read(1024)
        while file_data:
            client_socket.send(file_data)
            file_data = file.read(1024)
        client_socket.send(b'DONE')
        client_socket.recv(1024)
    client_socket.send("End".encode())
    print("Public key sent successfully")

def start_server(port, folder_path,public_key_path):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    send_files(client_socket, folder_path,public_key_path)
    print("Files sent successfully")
    print("Recieving results...... ")
    while True:
        print("Recving.....")
        filename = client_socket.recv(1024).decode()
        if filename == "End":
            break
        if not filename:
            break

        client_socket.send(b'ACK')

        with open(os.path.join("Encrypted_results", filename), 'ab') as file:
            file_data = client_socket.recv(1024)
            while file_data and file_data != b'DONE':
                file.write(file_data)
                file_data = client_socket.recv(1024)

        client_socket.send(b'ACK')

    print("Encrypted results recieved successfully")
    res = decrypt_results()
    serialized = pickle.dumps(res)
    client_socket.send(serialized)
    client_socket.close()

if __name__ == "__main__":
    if os.path.exists("Encrypted_results"):
        shutil.rmtree("Encrypted_results")

    os.makedirs("Encrypted_results")

    PORT = 12345
    FOLDER_PATH = "Encrypted_images"  
    public_key_path = "keys\public.txt"
    start_server(PORT, FOLDER_PATH,public_key_path)
