from EcoDatabase import EcoDatabase

db = EcoDatabase()



#def insert_data_point(self, node_id, boot_count, sensor_address, parameter_number, read_time, store_time, data_point):
#def insert_node_setup(self, node_id, boot_count, boot_time, store_time, comment="no comment"):
#def insert_node_sensor(self, node_id, boot_count, sensor_address, sensor_serial_number):
#def insert_gps_point(self, node_id, boot_count, read_time, store_time, latitude, longitude, altitude, siv):

db.insert_data_point(0, 1, 1, 1, 1, 1, 1)
db.insert_node_setup()
db.insert_node_sensor()
db.insert_gps_point()
