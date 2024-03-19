**Homomorphic encryption project**
1) This project demonstrates of Homomorphic encryption can be used to secure facial recognition system. 
2) Currently the project has 3 main modules : Cloud, Data_generation and Edge.  
3) Data generation acts as the source of data which generates data, in this project facial images are captured and sent to the Edge module.
4) The Edge module is the main module where the facial images recieved from the Data_generation module is encrypted homomorphically and stored in the local storage of edge module.
5) These images are encrypted and only verified people with the private can access the encrypted images.
6) Any third party client can access the encrypted database but cannot decrypt it since they do not have the private key.
7) Here the third party client is the Cloud module, Cloud module contains the program that act as the client.
8) The Client recieves the encrypted database and the public key where it will perform facial recognition using euclidean distance, the result is sent back to the edge server
9) The result is then interpreted by the edge server and returns the decrypted image of result.
