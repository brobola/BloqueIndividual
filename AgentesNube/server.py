from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from main import TrafficModel

import numpy as np
m = TrafficModel(10, 36, 36, 6)


def positionsToJSON():
    posDICT = []
    positions = m.positions
    print(positions)
    positions = sorted(positions, key= lambda id: id[0])
    print(positions)
    for p in positions:
        pos = {
            "id": p[0],
            "x": p[1][0],
            "z": p[1][1],
            "y": 0
            #"rotation": p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)


def semaforosToJSON():
    posDICT = []
    positions = m.semaforoPositions
    #positions = sorted(positions, key= lambda id: id[0])
    #lights = m.checkCarsInLane(36, 6)
    lights = m.getLights(36,6)
    for p in range(len(positions)):
        pos = {
            "x": positions[p][0],
            "z": positions[p][1],
            "y": 0,
            "luz": lights[p]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)


class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        #positions = updatePositions()
        m.step()
        self._set_response()
        resp = "{\"data\":" + positionsToJSON() + "}"
        self.wfile.write(resp.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))

        #positions = updatePositions()
        m.step()
        self._set_response()
        resp = "{\"data\":" + positionsToJSON() + "}"
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")  # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:  # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
