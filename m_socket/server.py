from .custom_types import m_session_socket

import random
import string
import threading

from socket import *
from typing import Callable, Any


class m_server_socket:
    host: str
    port: int
    socket_obj: socket

    sessions: list = []

    __receiving_data_on: Callable[[m_session_socket, bytes], Any]
    __connection_on: Callable[[m_session_socket], Any]
    __disconnection_on: Callable[[m_session_socket], Any]

    __shutdown = False

    def __init__(self, host: str, port: int,
                 receiving_data_on: Callable[[m_session_socket, bytes], Any] = None,
                 connection_on: Callable[[m_session_socket], Any] = None,
                 disconnection_on: Callable[[m_session_socket], Any] = None):
        self.host = host
        self.port = port

        self.__receiving_data_on = receiving_data_on
        self.__connection_on = connection_on
        self.__disconnection_on = disconnection_on

        self.socket_obj = socket(AF_INET, SOCK_STREAM)
        self.socket_obj.bind((host, port))

    def __check_id(self, socket_id: str):
        for session in self.sessions:
            if session.socket_id == socket_id:
                return False
        return True

    def __get_id(self):
        socket_id: str
        while 1:
            socket_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
            if self.__check_id(socket_id):
                break
        return socket_id

    def __receiving_client_data(self, conn: socket, ip: str):
        session_socket: m_session_socket = m_session_socket(conn, self.__get_id(), ip)
        self.sessions.append(session_socket)

        if self.__connection_on is not None:
            self.__connection_on(session_socket)

        while 1:
            try:
                data: bytes = conn.recv(1024)
                if data == b"" or self.__shutdown:
                    break
                if self.__receiving_data_on is not None:
                    threading.Thread(target=self.__receiving_data_on, args=(session_socket, data)).start()
            except Exception:
                break

        if not self.__shutdown:
            if self.__disconnection_on is not None:
                self.__disconnection_on(session_socket)

        self.sessions.remove(session_socket)

    def __waiting_for_client_connection(self):
        while 1:
            try:
                conn, ip = self.socket_obj.accept()
                threading.Thread(target=self.__receiving_client_data, args=(conn, ip)).start()
            except Exception:
                break

    def get_session_by_id(self, socket_id: str):
        for session_socket in self.sessions:
            if session_socket.socket_id == socket_id:
                return session_socket
        return None

    def listen(self):
        self.socket_obj.listen(1)
        threading.Thread(target=self.__waiting_for_client_connection).start()

    def close(self):
        self.__shutdown = True
        self.socket_obj.close()
