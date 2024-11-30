import time
import socket

def send_command(idnum, command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))
    message = f"{idnum}{command}"
    client.send(message.encode())

if __name__ == '__main__':
    client_id = "01"
    command = "forward"
    index = 0
    while True:
        some = input("click enter for movement: ")
        if (some == some):
            send_command(client_id, command)
            print(index)
            index = index + 1