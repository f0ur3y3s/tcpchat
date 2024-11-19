from flask import Flask, render_template, request, jsonify, Response
import socket
import threading
from queue import Queue

app = Flask(__name__)

# TCP client variables
client_socket = None
message_queue = Queue()  # Queue for storing incoming messages


# Function to receive messages from the TCP server
def receive_messages():
    global client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                message_queue.put(message)
        except:
            break


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send_message():
    global client_socket
    message = request.form.get("message")
    if message:
        try:
            client_socket.send(message.encode())
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "success"})


@app.route("/stream")
def stream_messages():
    def message_stream():
        while True:
            message = message_queue.get()
            yield f"data: {message}\n\n"

    return Response(message_stream(), content_type="text/event-stream")


def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 1337))
    threading.Thread(target=receive_messages, daemon=True).start()


if __name__ == "__main__":
    start_client()
    app.run(debug=True, port=8000)
