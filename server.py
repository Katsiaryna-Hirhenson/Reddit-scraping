"""This module launches local server at localhost:8087

It processes POST, GET, PUT, DELETE requests.
"""

import logging
import json
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

CURRENT_DATE = datetime.today().strftime('%Y%m%d%H%M')

HOST_NAME = "localhost"
HOST_PORT = 8087
FILE_NAME = 'reddit-' + str(CURRENT_DATE) + '.txt'

logging.basicConfig(filename='logname_server.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):
        """Processes POST requests.

        Receives data and writes it into .txt file.
        """
        if self.path.endswith('/posts'):
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            decoded_data = data.decode()
            line_to_add = decoded_data.split(';')
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), data.decode('utf-8'))

            with open(FILE_NAME, mode='a+', encoding='utf-8') as myfile:
                for line in myfile:
                    if line.startswith(str(line_to_add[0])):
                        self.send_response(404)
                        return

                myfile.write(decoded_data)
                data_dict = {line_to_add[0]: line_to_add[1:]}
                json_output = json.dumps(data_dict, indent=4)
                self.wfile.write(json_output.encode())

    def do_GET(self):
        """Returns data in json format.

        If url ends with '/posts' shows all data in json format.
        If url ends with '/post/unique id' shows single post with such unique id in json format.
        """
        if self.path.endswith('/posts'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            try:
                with open(FILE_NAME, 'r') as file:
                    for line in file:
                        line_to_add = line.split(';')
                        data_dict = {line_to_add[0]: line_to_add[1:]}
                        json_output = json.dumps(data_dict, indent=4)
                        self.wfile.write(json_output.encode())

            except FileNotFoundError as ex:
                print(ex)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        uuid = self.path.split('/')[-1]
        one_post = {}
        try:
            with open(FILE_NAME, 'r') as file:
                for line in file:
                    if line.startswith(uuid):
                        line_to_add = line.split(';')
                        one_post[uuid] = line_to_add[1:]
                json_output = json.dumps(one_post, indent=4)
                self.wfile.write(json_output.encode())

        except FileNotFoundError as ex:
            print(ex)

    def do_DELETE(self):
        """Deletes single post

        If post url ends with '/post/unique id' deletes single post with such unique id.
        """
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        logging.info("DELETE request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        uuid = self.path.split('/')[-1]
        key_in_file = False
        try:
            with open(FILE_NAME, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    line_to_add = line.split(';')
                    if uuid != line_to_add[0]:
                        file.write(line)
                    else:
                        key_in_file = True
                        self.wfile.write('Line was successfully deleted'.encode(encoding='utf_8'))
                file.truncate()

            if key_in_file:
                self.send_response(200)
            else:
                self.send_response(404)

        except FileNotFoundError as ex:
            print(ex)

    def do_PUT (self):
        """Updates single post.

        If url ends with '/post + unique id' updates single post with such unique id.
        """
        self.send_header('Content-Type', ' application/json')
        self.end_headers()
        logging.info("PUT request,\nPath: %s\nHeaders:\n%s\n",str(self.path),str(self.headers))
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        uuid = self.path.split('/')[-1]
        decoded_data = data.decode()
        line_to_update = decoded_data.split(';')
        key_in_file = False
        try:
            with open(FILE_NAME, 'r') as file:
                all_posts = file.readlines()
            with open(FILE_NAME, 'w') as file_with_updated_line:
                for line in all_posts:
                    if line.startswith(uuid):
                        key_in_file = True
                        new_line = str(uuid) + ';' + str(line_to_update[1:]) + '\n'
                        file_with_updated_line.write(new_line)
                        self.wfile.write('Line was successfully updated'.encode(encoding='utf_8'))
                    else:
                        file_with_updated_line.write(line)

            if key_in_file:
                self.send_response(200)
            else:
                self.send_response(404)

        except FileNotFoundError as ex:
            print(ex)


"""Creates HTTP-server."""

myServer = HTTPServer((HOST_NAME, HOST_PORT), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, HOST_PORT))

try:
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting httpd...\n')
    myServer.serve_forever()

except KeyboardInterrupt:
    pass

myServer.server_close()
logging.info('Stopping httpd...\n')
print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, HOST_PORT))
