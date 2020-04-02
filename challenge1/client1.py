#!/usr/bin/env python3

import socket
import sys

class Client():
    def __init__(self, ip, port, name="", debug=False):
        self.ip = ip
        self.port = port
        self.name = f"{name[:30]} {ip}:{port} - "
        self.debug = debug
        self.dprint("Connecting to Server")
        self.connect_to_server()

    #this is a debug print. Set debug to True to see
    #set debug to false to turn off
    def dprint(self, text):
        if self.debug:
            print(self.name + text.strip())

    #basic connect to client
    def connect_to_server(self):
        # Create a TCP/IP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = (self.ip, self.port)
        try:
            self.socket.connect(server_address)
            self.dprint('Connected to {} on port {}.'.format(self.ip, self.port))
        except OSError as e:
            self.dprint("ERROR establishing connection to {} on port {}".format(self.ip, self.port))
            sys.exit(1)

    #basic client_recv example
    def recv(self, endCharacter=None, decode_string='utf-8'):
        try:
            chunks = []
            chunk = b'starter'
            while chunk != b'' and chunk.decode('utf-8') != endCharacter:
                chunk = self.socket.recv(1)
                chunks.append(chunk)
            recv_msg = b''.join(chunks).decode(decode_string).strip()
            self.dprint("Received: " + recv_msg)
            return recv_msg
        except OSError as e:
            self.socket.close()
            self.dprint("ERROR receiving data from server: {}".format(e))
            sys.exit(1)

    def send(self, msg):
        self.dprint(msg.strip())
        try:
            self.socket.send(msg.encode('utf-8'))
        except OSError as e:
            self.dprint("ERROR sending data: {}".format(e))
            sys.exit(1)

    def send_and_close(self, msg, socket=None):
        self.send(msg, socket)
        self.socket.close()


def solve_question(ip, port):
    answers = []
    for i in range(1, 101):
        for j in range (1, 101):
            answers.append(i*j)
    # remove duplicates
    answers = list(dict.fromkeys(answers))
    for answer in answers:
        c = Client(ip=ip, port=port, debug=True)
        c.send(answer+'\n')
        # normally the end is a '\n'
        response = c.recv()
        if 'That is correct!' in response:
            break
    print(f"The answer is {answer} and the response is \"{response}\"")

if __name__ == "__main__":
    #if len(sys.argv) != 3:
    #    exit("Usage: {} <ip> <port>".format(sys.argv[0]))
    #ip=sys.argv[1]
    #port=int(sys.argv[2])
    ip='127.0.0.1'
    port=55555
    c = Client(ip=ip, port=port, debug=False)
    c.send('Hello\n')
    response = c.recv(endCharacter='?')
    parts = response[:-1].split(' ')
    answer = eval(parts[2]+parts[3]+parts[4])
    c.send(str(answer)+'\n')
    response = c.recv()
    print(f"The answer is {answer} and the response is \"{response}\"")

    # if question was not given
    #solve_question(ip, port)
