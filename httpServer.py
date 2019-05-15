# PUSH server refference https://pymotw.com/2/BaseHTTPServer/index.html#module-BaseHTTPServer

from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
from cgi import parse_header, parse_multipart
import json

import mysql.connector


class PostHandler(BaseHTTPRequestHandler):

    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        self.database = EcoDatabase()

    def do_POST(self):
        # Parse the form data posted

        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)
        print(data)

        nodeString = data['dev_id']
        payload = data['payload_fields']['data']
        print('Parsing ', payload)

        # authentication


        # extract node information
        node_id = str([s for s in nodeString.split() if s.isdigit()])
        print(node_id)
        print(type(node_id))


        if payload[0] == 'C':
            # config message
            self.parseTitleString(node_id, payload)
        else:
            # data message
            self.parseDataString(node_id, payload)


    def parseDataString(self, node_id, string):
        entries = string.split('&')

        boot_count = entries[0]

        read_time = datetimeFromUnixTime(entries[1])
        store_time = getCurrentTime()

        for entry in entries[2:]:
            e = entry.split(':')

            sensor_address = e[0]
            readings = e[1].split(',')

            for parameter_number, data_point in enumerate(readings):
                #writeDataToDatabase(int(node), int(boot_count), int(sensor), param, read_time, store_time, float(reading));
                self.database.insert_data_point(node_id, boot_count, sensor_address, parameter_number, read_time, store_time, data_point);

    def parseTitleString(self, node_id, string):
        entries = string[1:].split('&')

        boot_count = entries[0]

        boot_time = datetimeFromUnixTime(entries[1])
        store_time = getCurrentTime()

        self.database.insert_node_setup(node_id, boot_count, boot_time, store_time)

        for entry in entries[2:]:
            e = entry.split(':')

            sensor_address = e[0]
            sensor_serial_number = e[1]

            self.database.insert_node_sensor(node_id, boot_count, sensor_address, sensor_serial_number)


# wrapper for communicating with database
class EcoDatabase:

    # Initialize variables for communicating with data-base
    def __init__(self):
        self.engine = mysql.connector.connect(
               user="ecohydro",
               password="7fQh53G6D2BuCnT54hXH95CJx",
               host="ubc-ecohydro-nodes-mysql-database.cycweraudmq1.us-east-1.rds.amazonaws.com",
               port='3306',
               database='eco_nodes'
        )

        self.cur = self.engine.cursor()

    # Cleanup variables for talking to database
    def __del__(self):
        print("closed")
        self.cur.close()
        self.engine.close()


    def insert_data_point(self, node_id, boot_count, sensor_address, parameter_number, read_time, store_time, data_point):
        query = f'call eco_nodes.insert_data_point({node_id}, {boot_count}, {sensor_address}, {parameter_number}, \'{read_time}\', \'{store_time}\', {data_point});'
        print(query)
        self.cur.execute(query)
        self.engine.commit()

    def insert_node_sensor(self, node_id, boot_count, sensor_address, sensor_serial_number):
        query = f'call eco_nodes.insert_node_sensor({node_id}, {boot_count}, {sensor_address}, {sensor_serial_number});'
        print(query)
        self.cur.execute(query)
        self.engine.commit()

    def insert_node_setup(self, node_id, boot_count, boot_time, store_time, position="", comment=""):
        query = f'call eco_nodes.insert_node_setup({node_id}, {boot_count}, \'{boot_time}\', \'{store_time}\', {position}, {comment});'
        print(query)
        self.cur.execute(query)
        self.engine.commit()

    def insert_sensor_type(self, id, type, name, manufacturer, description):
        query = f'call eco_nodes.insert_sensor_type({id}, \'{type}\', \'{name}\', \'{manufacturer}\', \'{description}\');'
        print(query)
        self.cur.execute(query)
        self.engine.commit()



if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 5200), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
