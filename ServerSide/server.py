# Programmer: Alex
# Purpose: Server side code for the Turtle Race MMO
# Function: Using Socket to decode commands, using random to add an element of chance, and threading to optimize

import tkinter as TK
import socket
import threading
import turtle
import random
from queue import Queue

# Turtle race setup
turtlearr = []
startX = -800
startY = 325
place = 1
command_queue = Queue()

for pc in range(26):
    t = turtle.Turtle(shape="turtle")
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    t.fillcolor(color)
    t.pencolor(color)
    t.speed(0)
    t.goto(startX, startY)
    turtlearr.append(t)
    startY -= 25

# Function to process commands from the queue
def process_commands():
    global place
    while not command_queue.empty():
        idnum, command = command_queue.get()
        if command == "forward":
            turtlearr[idnum - 1].dot()
            dis = random.randint(10, 50)
            turtlearr[idnum - 1].forward(dis)
            if dis > 25 and random.randint(0, 10) > 9:
                turtlearr[idnum - 1].backward(dis)
            elif dis > 25 and random.randint(0, 10) > 4:
                turtlearr[idnum - 1].backward(dis / 2)

            if turtlearr[idnum - 1].xcor() > 800:
                turtlearr[idnum - 1].goto(0, turtlearr[idnum - 1].ycor())
                turtlearr[idnum - 1].write(f"Turtle from PC {idnum} got place {place}", font=("Arial", 24, "normal"))
                turtlearr[idnum - 1].turtlesize(10)
                place += 1
    turtle.ontimer(process_commands, 100)  # Schedule the next check

# Handle client commands
def handle_client(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            idnum = int(data[:2])
            command = data[2:]
            command_queue.put((idnum, command))  # Add to the queue
        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break
    conn.close()

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(5)
    print("Server started...")
    while True:
        try:
            conn, addr = server.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        except Exception as e:
            print(f"Server error: {e}")

if __name__ == '__main__':
    turtle.title('Server Turtle')
    threading.Thread(target=start_server, daemon=True).start()  # Run server in background
    process_commands()  # Start processing commands
    turtle.done()
