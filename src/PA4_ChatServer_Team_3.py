#!env python

"""Subnet Addressing in Mininet for CST311 Programming Assignment 4"""
__author__ = "Team 3 - GitReal"
__credits__ = [
  "Jerrett Rosario",
  "Teodora Balaj",
  "John Dorn",
  "David McFarland"
]

import socket as s
import ssl

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create threads for clients
from threading import Thread

# Set the global variables for the server name, port, key, and certificate
server_address = '10.0.5.3'
server_port = 12000
ssl_key_file = "/etc/ssl/demoCA/private/chatpa4.test-key.pem"
ssl_certificate_file = "/etc/ssl/demoCA/newcerts/chatpa4.test-cert.pem"

# Initialize a dictionary to hold the user attributes
users = {}

def connection_handler(username, secureConnSocket):
  while True:
    if username == 'X':
      # Read data from the new connection socket
      # Note: if no data has been sent this blocks until there is data
      query = secureConnSocket.recv(1024).decode()

      if query:
        # Add decoded query to users dict
        users[username]['message'] = query
        
        # Log query information
        log.info("Recieved query test \"" + str(query) + "\"")
        
        # Form the response from the username and message
        response = users[username]['username'] + ": " + users[username]['message']

        # Sent response over the network, encoding to UTF-8
        users['Y']['connection_socket'].send(response.encode())

    if username == 'Y':
      # Read data from the new connection socket
      # Note: if no data has been sent this blocks until there is data
      query = secureConnSocket.recv(1024).decode()

      if query:

        # Add decoded query to users dict
        users[username]['message'] = query
        
        # Log query information
        log.info("Recieved query test \"" + str(query) + "\"")
        
        # Form the response from the username and message
        response = users[username]['username'] + ": " + users[username]['message']

        # Sent response over the network, encoding to UTF-8
        users['X']['connection_socket'].send(response.encode())


def main():
  # Initialize the number of server connections to 0
  serverConnections = 0

  # Enable the TLS protocol
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

  # Set the version of the TLS connection to v1.2 as v1.3 sends session tickets after the handshake thus causing select() to always wait for data to be received and neither client waits for keyboard input
  # When the code gets to the select statement, it will always try to read from the socket because the server is still sending session tickets after the handshake, so there is technically data to be received
  # Because of this neither client will get to send a message
  # What should happen is there should be no data/tickets to be read in the socket, and select() should wait for data to arrive in the socket or for data to be typed in by the client
  context.maximum_version = ssl.TLSVersion.TLSv1_2

  # Load the key and cert files into the TLS context
  context.load_cert_chain(ssl_certificate_file, ssl_key_file)

  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign IP address and port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(2)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # If the amount of server requests has reached two, reset it back to zero
      # This helps when the clients disconnect/close their sockets, they'll be able to reconnect and be named X and Y again
      if serverConnections == 2:
        serverConnections = 0

      # When a client connects, create a new socket, record their address, and give each client its own thread
      connection_socket, address = server_socket.accept()
      
      # Wrap the connection socket in an SSL socket
      secureConnSocket = context.wrap_socket(connection_socket, server_side=True)

      # Name the first client to connect 'X' and the second 'Y'
      # Store their attributes in the dictionary
      if serverConnections == 0:
        username = 'X'
        users[username] = {'connection_socket':secureConnSocket, 'address':address, 'username':username, 'message':''}
      elif serverConnections > 0:
        username = 'Y'
        users[username] = {'connection_socket':secureConnSocket, 'address':address, 'username':username, 'message':''}

      log.info("Connected to client at " + str(address) + ". Calling it " + username + ".")

      # Create the thread for each client
      thread = Thread(target=connection_handler, args=(username, secureConnSocket))
      # Start the thread
      thread.start()
      # join() is not needed as this is an indefinite chat session, so there is no possibility that the threads will finish and join together on their own
      # The client will shutdown & close the socket which will ultimately kill the thread

      # Increment the amount of server connections by one
      serverConnections += 1
  finally:
    # Close the server socket
    server_socket.close()

if __name__ == "__main__":
  main()
