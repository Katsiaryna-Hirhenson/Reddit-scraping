"""This module launches local server at localhost:8087

It processes POST, GET, PUT, DELETE requests.
"""

import logging
import json
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

CURRENT_DATE = datetime.today().strftime('%Y.%m.%d.%H:%M')

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

        Receives data and writes it into txt file.
        If url ends with '/posts' adds new line to file.
        """
        if self.path.endswith('/posts'):
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), data.decode('utf-8'))
            decoded_data = data.decode()
            line_to_add = decoded_data.split(':')
            try:
                with open(FILE_NAME, 'r') as file:
                    for line in file:
                        if line.startswith(str(line_to_add[0])):
                            self.send_response(404)
                            return
                with open(FILE_NAME, 'a') as second_file:
                    new_line = str(line_to_add[0]) + ':' + str(line_to_add[1]) + '\n'
                    second_file.write(new_line)
                    self.send_response(201)
                    # file.write('\n')
                    new_line_dict = {new_line[0]: new_line[1]}
                    json_output = json.dumps(new_line_dict, indent=4)
                    self.wfile.write(json_output.encode())
            except Exception as ex:
                print(ex)
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        decoded_data = data.decode()
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), data.decode('utf-8'))
        try:
            with open(FILE_NAME, mode='w', encoding='utf-8') as myfile:
                for string in decoded_data:
                    myfile.write(string)
        except Exception as ex:
            print(ex)

    def do_GET(self):
        """Returns data in json format.

        If url ends with '/posts' shows all data in json format.
        If url ends with '/post + unique id' shows single post with such unique id in json format.
        """
        if self.path.endswith('/posts'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            one_post = {}
            all_posts = []
            try:
                with open(FILE_NAME, 'r') as file:
                    for line in file:
                        one_post[line[:32]] = line[35:]
                        all_posts[len(all_posts):] = [dict(one_post)]
                        one_post.clear()
                json_output = json.dumps(all_posts, indent=4)
                self.wfile.write(json_output.encode())
            except Exception as ex:
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
                        one_post[line[:32]] = line[35:]
                json_output = json.dumps(one_post, indent=4)
                self.wfile.write(json_output.encode())
        except Exception as ex:
            print(ex)

    def do_DELETE(self):
        """Deletes single post

        If post url ends with '/post + unique id' deletes single post with such unique id.
        """
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        uuid = self.path.split('/')[-1]
        key_in_file = False
        try:
            with open(FILE_NAME, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    file_uuid = line.split(' ')[0].replace(':', '')
                    if uuid != file_uuid:
                        file.write(line)
                    else:
                        key_in_file = True
                        self.wfile.write('Line was successfully deleted'.encode(encoding='utf_8'))
                file.truncate()

            if key_in_file:
                self.send_response(200)
            else:
                self.send_response(404)

        except Exception as ex:
            print(ex)

    def do_PUT (self):
        """Updates single post.

        If url ends with '/post + unique id' updates single post with such unique id.
        """
        self.send_header('Content-Type', ' application/json')
        self.end_headers()
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        uuid = self.path.split('/')[-1]
        decoded_data = data.decode()
        line_to_update = decoded_data.split(':')
        key_in_file = False
        try:
            with open(FILE_NAME, 'r') as file:
                all_posts = file.readlines()
            with open(FILE_NAME, 'w') as file_with_updated_line:
                for line in all_posts:
                    if line.startswith(uuid):
                        key_in_file = True
                        new_line = str(uuid) + ':' + str(line_to_update[1])
                        file_with_updated_line.write(new_line)
                        self.wfile.write('Line was successfully updated'.encode(encoding='utf_8'))
                    else:
                        file_with_updated_line.write(line)

            if key_in_file:
                self.send_response(200)
            else:
                self.send_response(404)

        except Exception as ex:
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
