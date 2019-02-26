#!/usr/bin/env python

import socket
import sys

client_socket = socket.socket(socket.AF_UNIX)
client_socket.connect("/tmp/vc-server")
client_socket.send(sys.argv[1].encode())
