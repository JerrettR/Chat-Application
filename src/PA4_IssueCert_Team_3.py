"""Chat client for CST311 Programming Assignment 3"""
__author__ = "Team 3 - GitReal"
__credits__ = [
  "Jerrett Rosario",
  "Teodora Balaj",
  "John Dorn",
  "David McFarland"
]

# The password, when prompoted, is "Nifty birds shoot acorns"

import os

try:
    # Create web server certificate
    os.chdir("..")
    os.chdir("/etc/ssl/demoCA")
    os.system("sudo openssl genrsa -out webpa4.test-key.pem 2048")
    common_name = input("Enter the common name for the web server: ")
    os.system('sudo openssl req -nodes -new -config /etc/ssl/openssl.cnf -key webpa4.test-key.pem -out webpa4.test.csr -subj "/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN=' + common_name + '"')
    os.system("sudo openssl x509 -req -days 365 -in webpa4.test.csr -CA cacert.pem -CAkey ./private/cakey.pem -CAcreateserial -out webpa4.test-cert.pem")
    os.system("sudo openssl x509 -text -noout -in webpa4.test-cert.pem")
    os.system("sudo mv webpa4.test-cert.pem newcerts") # Directory for tlswebserver.py
    os.system("sudo mv webpa4.test-key.pem private") # Directory for tlswebserver.py
except Exception as e:
    print(e)

try:
    # Create chat server certificate
    os.chdir("..")
    os.chdir("/etc/ssl/demoCA")
    os.system("sudo openssl genrsa -out chatpa4.test-key.pem 2048")
    common_name = input("Enter the common name for the chat server: ")
    os.system('sudo openssl req -nodes -new -config /etc/ssl/openssl.cnf -key chatpa4.test-key.pem -out chatpa4.test.csr -subj "/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN=' + common_name + '"')
    os.system("sudo openssl x509 -req -days 365 -in chatpa4.test.csr -CA cacert.pem -CAkey ./private/cakey.pem -CAcreateserial -out chatpa4.test-cert.pem")
    os.system("sudo openssl x509 -text -noout -in chatpa4.test-cert.pem")
    os.system("sudo mv chatpa4.test-cert.pem newcerts") # Directory for tlswebserver.py
    os.system("sudo mv chatpa4.test-key.pem private") # Directory for tlswebserver.py
except Exception as e:
    print(e)