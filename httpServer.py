# PUSH server refference https://pymotw.com/2/http.server/index.html#module-http.server

import time, threading, socket, socketserver, http.server
import json, datetime
import pymysql.cursors

# wrapper for communicating with database
class EcoDatabase:

    # Initialize variables for communicating with data-base
    def __init__(self):
        print("starting database")
        self.connection = pymysql.connect(host='ubc-ecohydro-nodes-mysql-database.cycweraudmq1.us-east-1.rds.amazonaws.com',
                                          port=3306,
                                          user='ecohydro',
                                          password='7fQh53G6D2BuCnT54hXH95CJx',
                                          database='eco_nodes',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        print("database started")


    # Cleanup variables for talking to database
    def __del__(self):
        print("closed")
        self.cursor.close()
        self.connection.close()


    def insert_data_point(self, node_id, boot_count, sensor_address, parameter_number, read_time, store_time, data_point):
        query = f'call eco_nodes.insert_data_point({node_id}, {boot_count}, {sensor_address}, {parameter_number}, \'{read_time}\', \'{store_time}\', {data_point});'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def insert_node_sensor(self, node_id, boot_count, sensor_address, sensor_serial_number):
        query = f'call eco_nodes.insert_node_sensor({node_id}, {boot_count}, {sensor_address}, {sensor_serial_number});'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def insert_node_setup(self, node_id, boot_count, boot_time, store_time, latitude='0.0', longitude='0.0', comment="test deployment"):
        query = f'call eco_nodes.insert_node_setup({node_id}, {boot_count}, \'{boot_time}\', \'{store_time}\', {latitude}, {longitude}, \'{comment}\');'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def insert_sensor_type(self, id, type, name, manufacturer, description):
        query = f'call eco_nodes.insert_sensor_type({id}, \'{type}\', \'{name}\', \'{manufacturer}\', \'{description}\');'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()



class PostHandler(http.server.BaseHTTPRequestHandler):

    database = EcoDatabase()

    def do_POST(self):
        # Parse the form data posted

        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)
        print(data)

        # authentication
        if (not data['app_id'] == 'ubc_econode_test_network'):
            return # message is not from a node

        nodeString = data['dev_id']
        payload = data['payload_fields']['data']
        print(threading.currentThread().getName(), 'parsing', payload)

        # extract node information
        node_id = ''.join([s for s in nodeString if s.isdigit()])

        if payload[0] == 'C':
            # config message
            self.parseTitleString(node_id, payload)
        else:
            # data message
            self.parseDataString(node_id, payload)

        return

    def parseDataString(self, node_id, string):
        entries = string.split('&')

        boot_count = entries[0]

        read_time = datetime.datetime.fromtimestamp(int(entries[1])).strftime('%Y-%m-%d %H:%M:%S')
        store_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        for entry in entries[2:]:
            e = entry.split(':')

            sensor_address = e[0]
            readings = e[1].split(',')

            for parameter_number, data_point in enumerate(readings):
                self.database.insert_data_point(node_id, boot_count, sensor_address, str(parameter_number), read_time, store_time, data_point)

    def parseTitleString(self, node_id, string):
        entries = string[1:].split('&')

        boot_count = entries[0]

        boot_time = datetime.datetime.fromtimestamp(int(entries[1])).strftime('%Y-%m-%d %H:%M:%S')
        store_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        self.database.insert_node_setup(node_id, boot_count, boot_time, store_time)

        for entry in entries[2:]:
            e = entry.split(':')

            sensor_address = e[0]
            sensor_serial_number = e[1]

            self.database.insert_node_sensor(node_id, boot_count, sensor_address, sensor_serial_number)


addr = ('0.0.0.0', 5200)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)
sock.listen(5)


# Launch multiple listener threads.
class Thread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
        self.daemon = True
        self.start()
    def run(self):
        httpd = http.server.HTTPServer(addr, PostHandler, False)

        # Prevent the HTTP server from re-binding every handler.
        # https://stackoverflow.com/questions/46210672/
        httpd.socket = sock
        httpd.server_bind = self.server_close = lambda self: None

        httpd.serve_forever()

[Thread(i) for i in range(20)]
time.sleep(9e9)
