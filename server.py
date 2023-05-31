import socket
import threading

HOST = 'localhost'
PORT = 12345

clients = {}  # Dictionnaire des clients connectés : {client_id: client_socket}

def moderate_message(client_socket):
    while True:
        try:
            # Recevoir le message du client
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

            # Extraire l'identifiant du destinataire et le message du format du message
            metadata, content = data.split(':')
            if metadata == "Username":
                clients[content] = client_socket
                print(f"User {content} is connected")
            elif metadata == "Sender, Recevers, Message":
                sender, user, message = content.split(",")
                # Vérifier si le destinataire existe dans la liste des clients connectés
                try:
                    if user in clients:
                        print("User found")
                        # Récupérer la socket du destinataire
                        recipient_socket = clients[user]

                        # Envoyer le message au destinataire
                        recipient_socket.sendall(f"Message, Sender:{message},{sender}".encode("utf-8"))
                    else:
                        print("User not found")
                except KeyError:
                    del clients[user]
                    client_socket.close()

            elif metadata == "Sender, Recevers, Audio":
                sender, user, audio = content.split(',')
                # Vérifier si le destinataire existe dans la liste des clients connectés
                try:
                    if user in clients:
                        print("Destinataire Trouvé")
                        # Récupérer la socket du destinataire
                        recipient_socket = clients[user]

                        # Envoyer le message au destinataire
                        recipient_socket.sendall(f"Audio, Sender:{audio},{sender}".encode("utf-8"))
                    else:
                        print("Destinataire non trouvé")
                except KeyError:
                    del clients[user]
                    client_socket.close()

            elif metadata == "Sender, Recevers, Audio, Camera":
                sender, user, audio, camera = content.split(',')

                # Vérifier si le destinataire existe dans la liste des clients connectés
                try:
                    if user in clients:
                        print("Destinataire Trouvé")
                        # Récupérer la socket du destinataire
                        recipient_socket = clients[user]

                        # Envoyer le message au destinataire
                        recipient_socket.sendall(f"Audio, Camera, Sender:{audio},{camera},{sender}".encode("utf-8"))
                    else:
                        print("Destinataire non trouvé")
                except KeyError:
                    del clients[user]
                    client_socket.close()
            elif metadata == "Sender, Friend":
                sender, user = content.split(",")
                recipient_socket.sendall(f"Friend:{sender}")


        except ConnectionError: 
            client_socket.close()
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Le serveur écoute sur le port", PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connexion établie depuis", client_address)
        thread = threading.Thread(target=moderate_message, args=(client_socket,))
        thread.start()


start_server()
