from m_socket import m_server_socket, m_session_socket

server_socket: m_server_socket


def connection_on(session_socket: m_session_socket):
    print(session_socket.socket_id, "connect")


def disconnection_on(session_socket: m_session_socket):
    print(session_socket.socket_id, "disconnect")


def receiving_data_on(session_socket: m_session_socket, data: bytes):
    print(session_socket.socket_id, data)
    session_socket.send(b"okay, i'm server")
    server_socket.close()


if __name__ == '__main__':
    server_socket = m_server_socket("127.0.0.1", 228,
                                    receiving_data_on=receiving_data_on,
                                    disconnection_on=disconnection_on,
                                    connection_on=connection_on)
    server_socket.listen()
    print("started server")
    while 1:
        pass
