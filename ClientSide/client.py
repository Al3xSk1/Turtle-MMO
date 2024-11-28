import socket
def send_command(idnum, command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))
    message = f"{idnum}{command}"
    client.send(message.encode())

if __name__ == '__main__':
    client_id = "01"
    while True:
        command = input('Enter command: ')
        send_command(client_id, command)