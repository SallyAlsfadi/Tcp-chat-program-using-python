import threading
import socket
ID = input('choose an Id >>> ')
client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',56000))
def client_receive():
    while True:
       # try:
            message = client.recv(1024).decode('utf-8')
            if message == "ID?":
                client.send(ID.encode('utf-8'))

            elif 'file' in message :
                file(message)

            else:
                print(message)
        

def file(message) :
    file_data = message.split(" :")
    filename = input('please enter a filename for the incoming file : ')
    file = open(filename,'w')
    file.write(file_data[1])
    file.close()
    print("file has been received successfully")

def client_send():
    while True:
        message = input("")
        client.send(message.encode('utf-8'))
receive_thread = threading.Thread(target = client_receive)
receive_thread.start()
send_thread = threading.Thread(target = client_send)
send_thread.start()
