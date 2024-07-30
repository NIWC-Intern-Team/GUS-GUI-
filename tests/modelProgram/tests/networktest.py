import socket

class NetworkHandler:
    def __init__(self):
        self.USV_IP = "127.0.0.1"  # Loopback IP address for testing
        self.USV_PORT = 11111  # Dummy port number

        self.udpOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP output

        self.CONTROL_IP = "127.0.0.1"  # Loopback IP address for testing
        self.CONTROL_PORT = 10101  # Dummy port number
        self.udpIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpIn.bind((self.CONTROL_IP, self.CONTROL_PORT))  # UDP input

# Example usage
handler = NetworkHandler()
