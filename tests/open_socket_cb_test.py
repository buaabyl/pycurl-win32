#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

import socket
import pycurl
import unittest

from . import appmanager
from . import util

setup_module, teardown_module = appmanager.setup(('app', 8380))

socket_open_called_ipv4 = False
socket_open_called_ipv6 = False
socket_open_called_unix = False
socket_open_address = None

def socket_open_ipv4(purpose, curl_address):
    family, socktype, protocol, address = curl_address
    global socket_open_called_ipv4
    global socket_open_address
    socket_open_called_ipv4 = True
    socket_open_address = address

    s = socket.socket(family, socktype, protocol)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    return s

def socket_open_ipv6(purpose, curl_address):
    family, socktype, protocol, address = curl_address
    global socket_open_called_ipv6
    global socket_open_address
    socket_open_called_ipv6 = True
    socket_open_address = address

    s = socket.socket(family, socktype, protocol)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    return s

def socket_open_unix(purpose, curl_address):
    family, socktype, protocol, address = curl_address
    global socket_open_called_unix
    global socket_open_address
    socket_open_called_unix = True
    socket_open_address = address

    sockets = socket.socketpair()
    sockets[0].close()
    return sockets[1]

class OpenSocketCbTest(unittest.TestCase):
    def setUp(self):
        self.curl = pycurl.Curl()

    def tearDown(self):
        self.curl.close()

    def test_socket_open(self):
        self.curl.setopt(pycurl.OPENSOCKETFUNCTION, socket_open_ipv4)
        self.curl.setopt(self.curl.URL, 'http://localhost:8380/success')
        sio = util.BytesIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, sio.write)
        self.curl.perform()

        assert socket_open_called_ipv4
        self.assertEqual(("127.0.0.1", 8380), socket_open_address)
        self.assertEqual('success', sio.getvalue().decode())

    @util.only_ipv6
    def test_socket_open_ipv6(self):
        self.curl.setopt(pycurl.OPENSOCKETFUNCTION, socket_open_ipv6)
        self.curl.setopt(self.curl.URL, 'http://[::1]:8380/success')
        sio = util.BytesIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, sio.write)
        try:
            # perform fails because we do not listen on ::1
            self.curl.perform()
        except pycurl.error:
            pass

        assert socket_open_called_ipv6

        assert len(socket_open_address) == 4
        assert socket_open_address[0] == '::1'
        assert socket_open_address[1] == 8380
        assert type(socket_open_address[2]) == int
        assert type(socket_open_address[3]) == int

    @util.min_libcurl(7, 40, 0)
    def test_socket_open_unix(self):
        self.curl.setopt(pycurl.OPENSOCKETFUNCTION, socket_open_unix)
        self.curl.setopt(self.curl.URL, 'http://localhost:8380/success')
        self.curl.setopt(self.curl.UNIX_SOCKET_PATH, '/tmp/pycurl-test-path.sock')
        sio = util.BytesIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, sio.write)
        try:
            # perform fails because we return a socket that is
            # not attached to anything
            self.curl.perform()
        except pycurl.error:
            pass

        assert socket_open_called_unix
        if util.py3:
            assert isinstance(socket_open_address, bytes)
            self.assertEqual(b'/tmp/pycurl-test-path.sock', socket_open_address)
        else:
            assert isinstance(socket_open_address, str)
            self.assertEqual('/tmp/pycurl-test-path.sock', socket_open_address)

    def test_socket_open_none(self):
        self.curl.setopt(pycurl.OPENSOCKETFUNCTION, None)

    def test_unset_socket_open(self):
        self.curl.unsetopt(pycurl.OPENSOCKETFUNCTION)
