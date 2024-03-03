import socket
import os
import tenseal as ts
from deepface import DeepFace
import utils
import pickle
import shutil


def compute_distances():
    sample_image_path = "input.jpg" #give path to your image

    context = ts.context_from(utils.read_data('Recv_files\public.txt'))
    image_proto = DeepFace.represent(sample_image_path,model_name='Facenet')[0]['embedding']
    image_ts = ts.plain_tensor(image_proto)
    for file in os.listdir('Recv_files'):
        if file == "public.txt":
            continue
        enc_image_proto = utils.read_data(f'Recv_files\{file}')
        enc_img = ts.lazy_ckks_vector_from(enc_image_proto)
        enc_img.link_context(context)
        euclidean_squard = image_ts - enc_img
        euclidean_squard = euclidean_squard.dot(euclidean_squard)
        utils.write_data(f"Result_files\{file[:-4]}.txt",euclidean_squard.serialize())
    print("Computation Done")
    

def receive_files(server_address, server_port, output_folder):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    while True:
        filename = client_socket.recv(1024).decode()
        if filename == "End":
            break
        if not filename:
            break

        client_socket.send(b'ACK')

        with open(os.path.join(output_folder, filename), 'ab') as file:
            file_data = client_socket.recv(1024)
            while file_data and file_data != b'DONE':
                file.write(file_data)
                file_data = client_socket.recv(1024)

        client_socket.send(b'ACK')

    print("Files received successfully.")
    print("Sending results..... ")
    compute_distances()
    print("Euclidean distance computed")

    for filename in os.listdir('Result_files'):
        file_path = os.path.join('Result_files', filename)
        with open(file_path, 'rb') as file:
            client_socket.send(filename.encode())
            client_socket.recv(1024)  

            file_data = file.read(1024)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(1024)

            client_socket.send(b'DONE')
            client_socket.recv(1024)

    client_socket.send("End".encode())
    print("Encrypted results sent successfully")
    sres = client_socket.recv(1024)
    res = pickle.loads(sres)
    if len(res) == 0:
        print("No Faces detected in database")
    else:
        for i in res:
            print(f"Faces detected : {i}")
    client_socket.close()

if __name__ == "__main__":
    if os.path.exists("Recv_files"):
        shutil.rmtree("Recv_files")
    if os.path.exists("Result_files"):
        shutil.rmtree("Result_files")

    os.makedirs("Recv_files")
    os.makedirs("Result_files")
    SERVER_ADDRESS = "localhost"
    SERVER_PORT = 12345
    OUTPUT_FOLDER = "Recv_files"  
    receive_files(SERVER_ADDRESS, SERVER_PORT, OUTPUT_FOLDER)

    

