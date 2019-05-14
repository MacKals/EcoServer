# PUSH server refference https://pymotw.com/2/BaseHTTPServer/index.html#module-BaseHTTPServer

from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
from cgi import parse_header, parse_multipart
import json

import mysql.connector


class PostHandler(BaseHTTPRequestHandler):
    
    # Initialize variables for communicating with data-base
   
       
    #engine = mysql.connector.connect(
    #        user="ecohydro",
    #        password="7fQh53G6D2BuCnT54hXH95CJx",
    #        host="ubc-ecohydro-nodes-mysql-database.cycweraudmq1.us-east-1.rds.amazonaws.com",
    #        port='3306',
    #        database='eco_nodes'
    #)

    #cur = engine.cursor()

    def do_POST(self):
        # Parse the form data posted

        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)
        nodeString = data['dev_id']
        payload = data['payload_fields']['data']
        print('Parsing ', payload)

        # authentication
        

        # extract node information
        node = [s for s in str.split() if s.isdigit()]
        print(node)
        print(type(node))
        

        if payload[0] == 'C':
            # config message
            parseTitleString(node, data)
        else:
            # data message
            parseDataString(node, data)


    def writeDataToDatabase(node, boot_count, sensor, param, read_time, store_time, reading):
        print(f'call eco_nodes.insert_data({node}, {boot_count}, {sensor}, {param}, \'{read_time}\', \'{store_time}\', {reading});')
        self.cur.execute(f'call eco_nodes.insert_data({node}, {boot_count}, {sensor}, {param}, \'{read_time}\', \'{store_time}\', {reading});')
        self.engine.commit()

    def insert_sensor_types():
        

    def writeConfigToDatabase()
        (id, type, name, manufacturer, description)
        
    def parseDataString(node, string):
        entries = string.split('&')

        read_time = datetimeFromUnixTime(entries[1])
        store_time = getCurrentTime()

        boot_count = entries[2]

        for entry in entries[3:]:
            e = entry.split(':')

            sensor = e[0]
            readings = e[1].split(',')

            for param, reading in enumerate(readings):
                #writeDataToDatabase(int(node), int(boot_count), int(sensor), param, read_time, store_time, float(reading));
                writeDataToDatabase(node, boot_count, sensor, param, read_time, store_time, reading);
    
    def parseTitleString(node, string):
        entries = string[1:].split('&')
        
        boot_time = datetimeFromUnixTime(entries[0])
        store_time = getCurrentTime()

        boot_count = entries[1]

        for entry in entries[2:]:
            writeSeria

        print("title string: " + string)
    
    # Cleanup variables for talking to database
#    def __del__(self):
 #       print("closed")
        #cur.close()
        #engine.close()

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 5200), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
