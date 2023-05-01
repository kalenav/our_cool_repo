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

def get_method(message):
    return message.split(" ")[0]

def get_post_json(message):
    return message.split("\n")[-1]

def assemble_response(text: str):
    method = get_method(text)
    if method == "GET":
        return get_request(text)
    elif method == "POST":
        return post_request(text)
    elif method == "OPTIONS":
        return options_request()

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

def get_request(text):
    requested_file_path = text.split(' ')[1]
    path = f'{DIRECTORY_PATH}{requested_file_path}'
    requested_content_type = mimetypes.types_map[f".{path.split('.')[1]}"]
    ok = True

    try:
        with open(path, 'rb') as file:
            response = file.read().decode()
    except Exception as e:
        ok = False
        response = 'Error 404: File not found'
    
    code, comment, content_type = ("200", "OK", requested_content_type) if ok else ("404", "Not Found", "text/html")
    additional_headers = {'Content-Type': content_type}
    header = f'{build_header(code, comment, additional_headers)}'

    return (header, response)

def options_request():
    return (build_header("200", "OK"), "")

def post_request(text):
    requested_file_path = text.split(' ')[1]
    path = f'{DIRECTORY_PATH}{requested_file_path}'
    ok = True

    try:
        with open(path, "w") as file:
            json.dump(json.loads(get_post_json(text)), file)
        with open(path, "rb") as file:
            response = True
    except Exception as e:
        ok = False
        response = False

    code, comment, content_type = ("200", "OK", 'text/html') if ok else ("500", "Internal Server Error", "application/json")
    additional_headers = {'Content-Type': content_type}
    header = f'{build_header(code, comment, additional_headers)}'

    return (header, response)
