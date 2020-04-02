import socket, random

num1        = random.randint(1,100)
num2        = random.randint(1,100)
prod        = num1 * num2
question    = "What is " + str(num1) + " * " + str(num2) + "?"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
print("Bind successful")
    
server.listen(5)
print("Server listening")

conn, addr  = server.accept()
print("Connection from:", addr)
print("Answer:" + str(prod))

while True:
    data         = conn.recv(4096)
    from_client = ''
    if not data:
        break
    #from_client += data.decode()     
    from_client += data.decode().strip()
    print(from_client)
    if (from_client   == "Hello"):
        conn.send(question.encode())
        continue
    elif (from_client == str(prod)):
        print("Client: " + from_client)
        conn.send(b"That is correct!")
        break
    else:
        print(from_client)
        conn.send(b"That is not correct")
        break
    
print("Closing Connection")
conn.close()
print("Client disconnected")
