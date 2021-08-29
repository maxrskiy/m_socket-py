import threading
from socket import *
from typing import Callable, Any


class m_client_socket:
    host: str
    port: int
    socket_obj: socket

    receiving_data_on: Callable[[bytes], Any]
    disconnection_on: Callable[[], Any]

    def __init__(self, host: str, port: int,
                 receiving_data_on: Callable[[bytes], Any] = None,
                 disconnection_on: Callable[[], Any] = None):
        self.host = host
        self.port = port

        self.receiving_data_on = receiving_data_on
        self.disconnection_on = disconnection_on

        self.socket_obj = socket(AF_INET, SOCK_STREAM)

    def __receiving_server_data(self):
        while 1:
            try:
                data = self.socket_obj.recv(1024)
                if data == b"":
                    break
                if self.receiving_data_on is not None:
                    threading.Thread(target=self.receiving_data_on, args=(data,)).start()
            except Exception:
                break
        if self.disconnection_on is not None:
            self.disconnection_on()

    def connect(self):
        try:
            self.socket_obj.connect((self.host, self.port))
            threading.Thread(target=self.__receiving_server_data).start()
        except Exception:
            return False
        return True

    def send(self, data: bytes):
        self.socket_obj.send(data)
