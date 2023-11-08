import serial
import time
from datetime import datetime as dt
from db import connect
from sqlalchemy import text
from serial.tools.list_ports import comports
import logging

log = logging.getLogger(__name__)

# make sure the 'COM#' is set according the Windows Device Manager
def connect_to_arduino(baud=9600, timeout=1):
    arduino_ports = [p for p in comports() if 'arduino' in p.description.lower()]
    if not arduino_ports:
        raise IOError("Unable to detect connected Arduino device!")
    log.info(f"connect to arduino on com port: {arduino_ports[0].device}")

    ser = serial.Serial(arduino_ports[0].device, baud, timeout=timeout)
    return ser


def read_temp_sensor(ser, conn):
    time.sleep(2)

    while True:
        line = ser.readline()   # read a byte
        if line:
            sensor_reading = line.decode()  # convert the byte string to a unicode string
            try:
                flds = sensor_reading.split()
                if flds[0].lower() == 'found':
                    continue
            except Exception as e:
                print("Exception occurred {e}")
            curr_time = dt.now()
            curr_time_str = curr_time.strftime("%Y-%m-%d_%H:%M:%S")
            print(f'{curr_time_str} {flds[0]} {flds[1]} {flds[2]}')
            insert_id = insert_into_db(flds, conn)
            print(f'Inserted sensor data - id {insert_id}')

    ser.close()

def insert_into_db(flds, conn=None):
    """ insert a new vendor into the vendors table """
    sql_insert = f"INSERT INTO  sensor_data (device_address, sensor_type, sensor_value) VALUES ('{flds[0]}','{flds[1]}','{flds[2]}' ) RETURNING id"
    query = text(sql_insert)
    id = conn.execute(query)
    conn.commit()
    return id.fetchone()

if __name__ == "__main__":
    ser = connect_to_arduino()
    conn = connect()
    read_temp_sensor(ser, conn)
    conn.close()
