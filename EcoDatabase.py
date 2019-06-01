
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
        query = 'INSERT INTO data_points(node_id, boot_count, sensor_address, parameter_number, read_time, store_time, data_point) '
        query += f'VALUES ({node_id}, {boot_count}, {sensor_address}, {parameter_number}, \'{read_time}\', \'{store_time}\', {data_point});'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    # insert new node master config from init message
    def insert_node_setup(self, node_id, boot_count, boot_time, store_time, comment="no comment"):
        query = 'INSERT INTO node_setup(node_id, boot_count, boot_time, store_time, comment) '
        query += f'VALUES ({node_id}, {boot_count}, \'{boot_time}\', \'{store_time}\', \'{comment}\');'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    # insert each sensor in init message
    def insert_node_sensor(self, node_id, boot_count, sensor_address, sensor_serial_number):
        query = 'INSERT INTO node_sensors(node_id, boot_count, sensor_address, sensor_serial_number) '
        query += f'VALUES ({node_id}, {boot_count}, \'{sensor_address}\', \'{sensor_serial_number}\');'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def insert_gps_point(self, node_id, boot_count, read_time, store_time, latitude, longitude, altitude, siv):
        query = 'INSERT INTO node_setup(node_id, boot_count, read_time, store_time, latitude, longitude, altitude, siv) '
        query += f'VALUES ({node_id}, {boot_count}, \'{read_time}\', \'{store_time}\', {latitude}, {longitude}, {altitude}, {siv},);'
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    # def insert_sensor_type(self, id, type, name, manufacturer, description):
    #     query = f'call eco_nodes.insert_sensor_type({id}, \'{type}\', \'{name}\', \'{manufacturer}\', \'{description}\');'
    #     print(query)
    #     self.cursor.execute(query)
    #     self.connection.commit()
