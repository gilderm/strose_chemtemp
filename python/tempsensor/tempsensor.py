import serial
import time
from datetime import datetime as dt
import db as db
import psycopg2

# make sure the 'COM#' is set according the Windows Device Manager
def read_temp_sensor(chemdb):
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(5)

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
            insert_id = insert_into_db(chemdb, flds)
            print(f'Inserted sensor data - id {insert_id}')

    ser.close()

def insert_into_db(db, flds):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO sensor_data(device_address, sensor_type, sensor_value)
             VALUES(%s, %s, %s) RETURNING id;"""
    conn = None
    id = None
    try:
        # read database configuration
        # params = config()
        # connect to the PostgreSQL database
        #conn = psycopg2.connect(**params)
        # create a new cursor
        cur = db.conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (flds[0],flds[1],flds[2]))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        db.conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return id

if __name__ == "__main__":
    chemdb = db.DatabaseUtils('localhost','chem','postgres', '1postgres1')
    read_temp_sensor(chemdb)