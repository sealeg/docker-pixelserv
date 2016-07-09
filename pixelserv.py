#!/usr/bin/env python

#
# A Pixel Server
#

import SocketServer
import struct, sys, signal, time

from datetime import datetime

class PixelRequestHandler(SocketServer.StreamRequestHandler):

    pixel = struct.pack('<43B', 
            71, 73, 70, 56, 57, 97, 1, 0, 1, 0, 128, 0, 0, 255, 255, 255, 
            0, 0, 0, 33, 249, 4, 1, 0, 0, 0, 0, 44, 0, 0, 0, 0, 1, 0, 1, 
            0, 0, 2, 2, 68, 1, 0, 59)

    def _parse_request(self):
        self.request_data = {'verb': '', 'path': '', 'version': '', 'host': ''}
        line = self.rfile.readline(65536)
        words = line.rstrip('\r\n').split()
        if len(words) == 3:
            self.request_data['verb']    = words[0]
            self.request_data['path']    = words[1]
            self.request_data['version'] = words[2]
        elif len(words) == 2:
            self.request_data['verb']    = words[0]
            self.request_data['path']    = words[1]
        line = self.rfile.readline(65536)
        while line[0:4].lower() != 'host':
            line = self.rfile.readline(65536)
        else:
            self.request_data['host'] = line[6:].rstrip('\r\n')

    def handle(self):
        self.wfile.write("HTTP/1.1 200 OK\r\n");
        self.wfile.write("Content-type: image/gif\r\n");
        self.wfile.write("Accept-ranges: bytes\r\n");
        self.wfile.write("Content-length: 43\r\n\r\n");
        self.wfile.write(self.pixel);
        self._parse_request()
        ts   = datetime.now().isoformat(' ')
        ip   = self.client_address[0]
        port = self.client_address[1]
        verb = self.request_data['verb']
        host = self.request_data['host']
        path = self.request_data['path']
        print '%s %s:%s %s %s%s' % (ts, ip, port, verb,  host, path)

def sighandler(signal, frame):
    raise Exception('Recieved %s signal' % signal)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000
    server = SocketServer.TCPServer((HOST, PORT), PixelRequestHandler)
    try:
        signal.signal(signal.SIGINT, sighandler)
        server.serve_forever()
    except:
        server.server_close()
        print '\nExiting...'
        sys.exit(0)

