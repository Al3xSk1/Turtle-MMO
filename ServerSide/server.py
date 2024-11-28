import tkinter as TK
import socket
import threading
import turtle 
import random

turtlearr = []

for pc in range(26):
    turtlearr.append(turtle.Turtle(shape="turtle"))
    color = "%06x" % random.randint(0, 0xFFFFFF)
    turtlearr[pc].pencolor(color)

def handle_client(conn, addr):
    while True:
        data = conn.recv(1024).decode()
        idnum = int(data[:2])
        command = data[2:]
        if not data:
            break
        if (command == "forward"):
            turtlearr[idnum].forward(100)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        print('Connected to:', addr)
        threading.Thread(target=handle_client, args=(conn, addr)).start()
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")

if __name__ == '__main__':
    turtle.title('Server Turtle')
    turtle.Screen().setup(800, 600)
    threading.Thread(target=start_server).start()
    turtle.done()