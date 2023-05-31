import socket
import pyaudio
import time
import cv2

HOST = 'localhost'
PORT = 12345

# Paramètres de l'audio
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

class Client:
    def __init__(self, username) -> None:
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        # Send Username
        self.send_username()

        # Variable
        self.is_calling = False
        self.is_camera_call = False
        
        # Muted
        self.camera_enabled = False
        self.is_muted = True
        
        # Créer l'objet PyAudio
        self.audio = pyaudio.PyAudio()

        # Get Camera and Micro
        self.microphone = self.get_micro()
        self.camera = self.get_camera()

    def get_camera(self):
        try:
            vid = cv2.VideoCapture(0)
            return vid
        except OSError:
            return
    
    def get_micro(self):
        # Ouvrir le flux audio en entrée
        try:
            stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            return stream
        except OSError:
            return

    def send_video(self):
            time.sleep(0.1)
            ret, frame = self.camera.read()

            # Convert frame to JPEG format
            _, encoded_frame = cv2.imencode(".jpg", frame)
            image_bytes = encoded_frame.tobytes()

            # Send the frame to the server
            self.send_message(self.username, f"Camera:{image_bytes}".encode())

    def send_audio(self):
            time.sleep(0.1)
            # Lire les données audio du flux
            data = f"Sender, Recevers, Audio:{self.username},{self.username},{self.microphone.read(CHUNK)}"

            # Send the frame to the server
            self.client_socket.sendall(data.encode())

    def send_username(self):
        data = f"Username:{self.username}"
        self.client_socket.sendall(data.encode())

    def send_message(self, recipient_id, message):
        # Format du message : "destinataire:message"
        data = f"Sender, Recevers, Message:{self.username},{recipient_id},{message}"
        self.client_socket.sendall(data.encode())

    def send_friend_request(self, username):
        # Format du message : "destinataire:message"
        data = f"Sender, Friend:{self.username},{username}"
        self.client_socket.sendall(data.encode())

    def send_call(self, recipient_id, audio, video=None):
        if video == None:
            # Format du message : "destinataire:message"
            data = f"Sender, Recevers, Audio:{self.username},{recipient_id},{audio}"
            self.client_socket.sendall(data.encode())
        else:
            # Format du message : "destinataire:message"
            data = f"Sender, Recevers, Audio, Camera:{self.username},{recipient_id},{audio},{video}"
            self.client_socket.sendall(data.encode())

    def receive_message(self):
        data = self.client_socket.recv(1024).decode()
        metadata, content = data.split(":")
        if metadata == "Message, Sender":
            message, sender = content.split(",")
            print(f"{sender} send: {message}")
            return "Message", message, sender
        elif metadata == "Audio, Sender":
            message, sender = content.split(",")
            return "Audio", message, sender
        elif metadata == "Audio, Camera, Sender":
            audio, camera, sender = content.split(",")
            return "Camera", f"{camera},{audio}", sender
        elif metadata == "Friend":
            sender = content
            return "Friend", sender, sender


