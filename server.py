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
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        decoded_data = data.decode()
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), data.decode('utf-8'))

        with open(FILE_NAME, mode='w',encoding='utf-8') as myfile:
            for string in decoded_data:
                myfile.write(string)

        if self.path.endswith('/posts'):
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                         str(self.path), str(self.headers), data.decode('utf-8'))
            decoded_data = data.decode()
            line_to_add = decoded_data.split(':')
            with open(FILE_NAME, 'r') as file:
                for line in file:
                    if line.startswith(str(line_to_add[0])):
                        print('This key is already in use')
                        return
            with open(FILE_NAME, 'a') as file:
                new_line = str(line_to_add[0]) + ':' + str(line_to_add[1])
                file.write(new_line)
                file.write('\n')
                new_line_dict = {new_line[0]: new_line[1]}
                json_output = json.dumps(new_line_dict, indent=4)
                self.wfile.write(json_output.encode())

    def do_GET(self):
        if self.path.endswith('/posts'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            one_post = {}
            all_posts = []
            with open(FILE_NAME, 'r') as file:
                for line in file:
                    one_post[line[:32]] = line[35:]
                    all_posts[len(all_posts):] = [dict(one_post)]
                    one_post.clear()
            json_output = json.dumps(all_posts, indent=4)
            self.wfile.write(json_output.encode())

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        uuid = self.path.split('/')[-1]
        one_post = {}
        with open(FILE_NAME, 'r') as file:
            for line in file:
                if line.startswith(uuid):
                    one_post[line[:32]] = line[35:]
            json_output = json.dumps(one_post, indent=4)
            self.wfile.write(json_output.encode())

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        uuid = self.path.split('/')[-1]
        with open(FILE_NAME, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                file_uuid = line.split(' ')[0].replace(':', '')
                if uuid != file_uuid:
                    file.write(line)
            file.truncate()
        self.wfile.write('Line was successfully deleted'.encode(encoding='utf_8'))

    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        uuid = self.path.split('/')[-1]
        decoded_data = data.decode()
        line_to_update = decoded_data.split(':')
        with open(FILE_NAME, 'r') as file:
            all_posts = file.readlines()
        with open(FILE_NAME, 'w') as file_with_updated_line:
            for line in all_posts:
                if line.startswith(uuid):
                    new_line = str(line_to_update[0]) + ':' + str(line_to_update[1]) + '\n'
                    file_with_updated_line.write(new_line)
                    self.wfile.write('line was successfully updated!'.encode())
                else:
                    file_with_updated_line.write(line)


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

#