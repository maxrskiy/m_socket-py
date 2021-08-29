from m_socket import m_client_socket

client_socket: m_client_socket


def disconnection_on():
    print("disconnected")


def receiving_data_on(data: bytes):
    print("server:", data)


if __name__ == '__main__':
    client_socket = m_client_socket("127.0.0.1", 228,
                                    receiving_data_on=receiving_data_on,
                                    disconnection_on=disconnection_on)
    if client_socket.connect():
        print("started client")
        client_socket.send(b"hello, i'm client")
    else:
        print("not started client")
