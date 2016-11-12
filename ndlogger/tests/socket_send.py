#!/usr/bin/env python

import socket

from os.path import join, dirname

TCP_IP = "127.0.0.1"
TCP_PORT = 27500

with open(join(dirname(__file__), 'log.txt'), 'rb') as fp:
    for line in fp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        sock.send(line)
        sock.close()
