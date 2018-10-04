#!/usr/bin/env python3

import socket
import sys

clientsocket = socket.socket()
clientsocket.connect(('localhost', 2357))
clientsocket.send(sys.argv[1].encode())
