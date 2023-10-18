#!env python

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "Team 3 - GitReal"
__credits__ = [
  "Jerrett Rosario",
  "Teodora Balaj",
  "John Dorn",
  "David McFarland"
]

# Import statements
import socket as s
import select
import sys
import ssl

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables for the server name and port
server_name = 'www.chatpa4.test'
server_port = 12000

def main():
  # Create the context for an SSL/TLS socket
  context = ssl.create_default_context()

  # Set the TLS version to 1.2, as v1.3 sends session tickets after the handshake, making recv() have data in the read buffer, preventing the client from accepting input
  # When the code gets to the select statement, it will always try to read from the socket because the server is still sending session tickets after the handshake, so there is technically data to be received
  # Because of this neither client will get to send a message
  # What should happen is there should be no data/tickets to be read in the socket, and select() should wait for data to arrive in the socket or for data to be typed in by the client
  context.maximum_version = ssl.TLSVersion.TLSv1_2

  # Create socket
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  # Wrap the socket in an SSL socket
  secureClientSocket = context.wrap_socket(client_socket, server_hostname=server_name)
  
  try:
    # Establish TLS-enabled TCP connection
    secureClientSocket.connect((server_name, server_port))
  except Exception as e:
    log.exception(e)
    log.error("***Advice:***")
    if isinstance(e, s.gaierror):
      log.error("\tCheck that server_name and server_port are set correctly.")
    elif isinstance(e, ConnectionRefusedError):
      log.error("\tCheck that server is running and the address is correct")
    else:
      log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
    exit(8)
  
  # Wrap in a try-finally to ensure the socket is properly closed regardless of errors
  try:
    break_loop = True

    while break_loop:
      # Create a list to hold stdin and the SSL-client socket
      sockets = [sys.stdin, secureClientSocket]
      
      try:
        # select() tells the kernel to notify when any of the descriptors/sockets are ready for read or write
        input_socket, output_socket, err_socket = select.select(sockets, [], [])
      except Exception as e:
        print("ERROR: ")
        print(e)

      # Loop through the available sockets
      for socket in input_socket:
        # The if-else statement will make it possible to read or write instantly
        if socket == secureClientSocket:
          # Read response from server
          server_response = secureClientSocket.recv(1024)

          # Decode server response from UTF-8 bytestream
          server_response_decoded = server_response.decode()
          
          # Print output from server
          print(str(server_response_decoded))      

          if 'Bye' in server_response_decoded:
            # secureClientSocket.close()
            # client_socket.close()
            break_loop = False
            break    

        else:
          # Get input from user
          user_input = input()

          # Set data across socket to server
          #  Note: encode() converts the string to UTF-8 for transmission
          secureClientSocket.send(user_input.encode())

          if user_input == 'Bye':
            break_loop = False
            break
  
  finally:
    # Shutdown & close both sockets prior to exit
    client_socket.close()
    secureClientSocket.shutdown(s.SHUT_RDWR)
    secureClientSocket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()