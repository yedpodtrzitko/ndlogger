#!/usr/bin/env python

import socket

from os.path import join, dirname

UDP_IP = "127.0.0.1"
UDP_PORT = 27500

with open(join(dirname(__file__), 'log.txt'), 'rb') as fp:
    for line in fp:
        print 'seding lne'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(line, (UDP_IP, UDP_PORT))
        sock.close()
