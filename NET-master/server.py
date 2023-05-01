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

def build_header(status_code, status_text, additional_headers = {}):
    headers = []
    header_dict = dict({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Method': 'POST, GET, OPTIONS'
    })
    header_dict.update(additional_headers)
    for header in header_dict:
        headers.append(f'{header}: {header_dict[header]}')
    headers = "\n".join(headers)
    return f'''HTTP/1.1 {status_code} {status_text}\r{headers}\r'''
