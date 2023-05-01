import socket
import mimetypes
import logging
import json
import argparse

logging.basicConfig(filename="log.txt", level=logging.INFO, filemode='w')

def listen(port, path):
    global DIRECTORY_PATH
    DIRECTORY_PATH = path

    # first arg = address family, AF_INET = IPv4, AF_INET6 = IPv6
    # second arg = type of socket(protocol), SOCK_STREAM = TCP, SOCK_DGRAM = UDP

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", port))
        logging.info(f"The server is running on http://localhost:{port}.")
        # 5 = max queued connections
        server.listen(5)
        logging.info("Waiting for connection requests.")
        while True:
            conn, addr = server.accept()
            addr = f"{addr[0]}:{addr[1]}"
            logging.info(f"Established a connection with {addr}.")
