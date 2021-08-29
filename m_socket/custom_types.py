import socket


class m_session_socket:
    client_socket: socket

    socket_id: str
    ip: str

    def __init__(self, client_socket: socket, socket_id: str, ip: str):
        self.client_socket = client_socket
        self.socket_id = socket_id
        self.ip = ip

    def send(self, data: bytes):
        self.client_socket.send(data)
