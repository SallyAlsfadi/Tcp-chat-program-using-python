import threading 
import socket
host='127.0.0.1'
port= 56000 
server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients = dict()

def broadcast(message, Clientip):

    for id, client in clients.items() :
        if(client == Clientip) :
          continue
        client.send(message)

def private (message, target, client) :
    id = target.split(" to ")[1]
    clients[id].send(f'private chat {findClient(client)}: {message}'.encode('utf-8'))
    while True :
      message = client.recv(1024).decode('utf-8')
      if 'exit' in message :
        clients[id].send(f'{findClient(client)} has exit private chat'.encode('utf-8'))
        break
      clients[id].send(f'{findClient(client)}: {message}'.encode('utf-8'))

def groups(message, target, client) :
    packet = target.split(" with ")
    groupMember = packet[1].split(",")
    for member in groupMember :
      clients[member].send(f'group chat {findClient(client)}: {message}'.encode('utf-8'))
    while True :
      message = client.recv(1024).decode('utf-8')
      if 'exit' in message :
        clients[id].send(f'{findClient(client)} has exit group chat'.encode('utf-8'))
        break
      for member in groupMember :
        clients[member].send(f'{findClient(client)}: {message}'.encode('utf-8'))

def handle_client(client):

    while True:

       try :
            message = client.recv(1024)
            packet = parse_text(message)

            if message.decode('utf-8') == 'id?' :
               for id in clients.keys() :
                   if client == clients[id] :
                      continue
                   client.send(id.encode('utf-8'))

            if 'file' in packet[1] :
               file(client, packet[0], packet[1])
           
            elif 'private' in packet[1] :
               private(packet[0], packet[1], client)

            elif 'group' in packet[1] :
               groups(packet[0], packet[1], client)

            else :

               broadcast(f'{findClient(client)}: {packet[0]}'.encode('utf-8'), client)

       except :

            id = findClient(client)
            del clients[id]
            client.close()
            broadcast(f'{id} has left the chat room'.encode('utf-8'), client)
            break

def parse_text(message) :

    text = message.decode(('ascii'))
    textList = text.split("//")
    text = textList[0]
    target = "all"
    if len(textList) > 1 :
       target = textList[0]
       text = textList[1]
    return (text, target)

def findClient(searchClient) :
  for id, client in clients.items() :
    if client == searchClient :
       return id

def file(client, fileName, sentTo):
    file = open(fileName, "r")
    file_data = f'file :{file.read(1024)}'.encode('utf-8')
    if 'private' in sentTo :
        private(file_data, sentTo, client)
    elif 'group' in sentTo :
        groups(file_data, sentTo, client)
    else :
        broadcast(file_data, client)
    print("Data has been transmitted successfully ")

def receive():

    while True:
        print('Server is sunning and listening .....')
        client, Address = server.accept()
        print(f'The connection is being astablished with {str(Address)} ')
        client.send('ID?'.encode('UTF-8'))
        ID = client.recv(1024).decode('UTF-8')
        clients[ID] = client
        print(f'The Id of this client is {ID}'.encode('UTF-8'))
        broadcast(f'{ID} has connected to chat '.encode('utf-8'), client)
        client.send('you are now connected'.encode('utf-8'))
        thread= threading.Thread(target = handle_client, args = (client,))
        thread.start()
if __name__=="__main__":
    receive();
