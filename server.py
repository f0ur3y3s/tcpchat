import socket
import threading

clients = []


def handle_client(client_socket: socket.socket, address):
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{address}: {message.decode('utf-8')}")
            broadcast(message, client_socket)
    except:
        pass
    finally:
        clients.remove(client_socket)
        client_socket.close()


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                pass


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 1337))
    server.listen(5)
    print("Server started on port 1337.")
    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        print(f"Connection from {address}")
        threading.Thread(target=handle_client, args=(client_socket, address)).start()


if __name__ == "__main__":
    main()
