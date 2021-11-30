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
        if self.path.endswith('/posts/'):
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            length = self.headers['content-length']
            encoded_post = self.rfile.read(int(length))
            decoded_post = encoded_post.decode()
            split_post_into_key_and_data = decoded_post.split(';')
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), encoded_post.decode('utf-8'))

            with open(FILE_NAME, mode='a+', encoding='utf-8') as file:
                for line in file:
                    if line.startswith(str(split_post_into_key_and_data[0])):
                        self.send_response(404)
                        return

                file.write(decoded_post)
                post_in_dict_for_json = {split_post_into_key_and_data[0]: split_post_into_key_and_data[1:]}
                json_output = json.dumps(post_in_dict_for_json, indent=4)
                self.wfile.write(json_output.encode())

            return

    def do_GET(self):
        """Returns data in json format.

        If url ends with '/posts' shows all data in json format.
        If url ends with '/post/unique id' shows single post with such unique id in json format.
        """
        try:
            f = open(FILE_NAME, 'r')
            f.close()

        except FileNotFoundError as ex:
            self.send_response(404)
            logging.exception(ex)
            return

        uuid = self.path.split('/')[-2]
        if uuid == 'posts':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            with open(FILE_NAME, 'r') as file:
                for line in file:
                    split_post_into_key_and_data = line.split(';')
                    post_in_dict_for_json = {split_post_into_key_and_data[0]: split_post_into_key_and_data[1:]}
                    json_output = json.dumps(post_in_dict_for_json, indent=4)
                    self.wfile.write(json_output.encode())

            return

        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            uuid = self.path.split('/')[-2]
            post_in_dict_for_json = {}
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

            with open(FILE_NAME, 'r') as file:
                for line in file:
                    if line.startswith(uuid):
                        split_post_into_key_and_data = line.split(';')
                        post_in_dict_for_json[uuid] = split_post_into_key_and_data[1:]
                        json_output = json.dumps(post_in_dict_for_json, indent=4)
                        self.wfile.write(json_output.encode())
                        return
                    else:
                        continue

    def do_DELETE(self):
        """Deletes single post

        If post url ends with '/post/unique id' deletes single post with such unique id.
        """
        try:
            f = open(FILE_NAME, 'r')
            f.close()

        except FileNotFoundError as ex:
            self.send_response(404)
            logging.exception(ex)
            return

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        logging.info("DELETE request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        uuid = self.path.split('/')[-2]
        uuid_in_file = False

        with open(FILE_NAME, 'r+') as file:
            all_posts = file.readlines()
            file.seek(0)
            for line in all_posts:
                split_post_into_key_and_data = line.split(';')
                if uuid != split_post_into_key_and_data[0]:
                    file.write(line)
                else:
                    uuid_in_file = True
                    self.wfile.write('Line was successfully deleted'.encode(encoding='utf_8'))
            file.truncate()

        if uuid_in_file:
            self.send_response(200)
        else:
            self.send_response(404)

        return

    def do_PUT(self):
        """Updates single post.

        If url ends with '/post + unique id' updates single post with such unique id.
        """
        try:
            f = open(FILE_NAME, 'r')
            f.close()

        except FileNotFoundError as ex:
            self.send_response(404)
            logging.exception(ex)
            return

        self.send_header('Content-Type', ' application/json')
        self.end_headers()
        logging.info("PUT request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        length = self.headers['content-length']
        encoded_post = self.rfile.read(int(length))
        uuid = self.path.split('/')[-2]
        decoded_post = encoded_post.decode()
        split_post_into_key_and_data = decoded_post.split(';')
        key_in_file = False

        with open(FILE_NAME, 'r') as file:
            all_posts = file.readlines()
        with open(FILE_NAME, 'w') as file_with_updated_line:
            for line in all_posts:
                if line.startswith(uuid):
                    key_in_file = True
                    updated_line = str(uuid) + ';' + str(split_post_into_key_and_data[1:]) + '\n'
                    file_with_updated_line.write(updated_line)
                    self.wfile.write('Line was successfully updated'.encode(encoding='utf_8'))
                else:
                    file_with_updated_line.write(line)

        if key_in_file:
            self.send_response(200)
        else:
            self.send_response(404)

        return


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
