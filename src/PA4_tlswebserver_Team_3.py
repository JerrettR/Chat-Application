#!/usr/bin/env python3

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "Team 3 - GitReal"
__credits__ = [
  "Jerrett Rosario",
  "Teodora Balaj",
  "John Dorn",
  "David McFarland"
]

import http.server
import ssl

# Variables, including location of server certificate and private key file
server_address = "www.webpa4.test" # h2, IP Address 10.0.3.3
server_port = 4443
ssl_key_file = "/etc/ssl/demoCA/private/webpa4.test-key.pem"
ssl_certificate_file = "/etc/ssl/demoCA/newcerts/webpa4.test-cert.pem"

#Context is the TLS Server with its certificate file and key file location
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(ssl_certificate_file, ssl_key_file)

## Don't modify anything below
httpd = http.server.HTTPServer((server_address, server_port),http.server.SimpleHTTPRequestHandler)
httpd.socket = context.wrap_socket(httpd.socket,server_side=True)

print("Listening on port", server_port)
httpd.serve_forever()