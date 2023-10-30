import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime, timezone
from db import connect
from sqlalchemy import text
import numpy as np
from numpy import array


last_timestamp = None

# This function is called periodically from FuncAnimation


def realtime_plot(conn, dev_id):
    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    def animate(i,xs,ys):
        global last_timestamp
        # Read temperature data from the database from last timestamp
        temp_c, temp_time, last_timestamp = read_from_db(conn, last_timestamp, dev_id)
        # Add x and y to lists
        xs = xs+temp_time
        ys = ys+temp_c

        # Limit x and y lists to 20 items
        #xs = xs[-500:]
        #ys = ys[-500:]

        #print(f"last timestamp: {last_timestamp}")
        #print(f"xs: {xs}")
        #print(f"ys: {ys}")

        # if no new data just return
        if len(xs) < 0 or len(ys) < 0:
            return
        
        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        ax.set_ylim([25,100])

        myFmt = mdates.DateFormatter("%m-%d %H:%M:%S")
        ax.xaxis.set_major_formatter(myFmt)
        #fig.autofmt_xdate()

        # Format plot'
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=0.20)
        plt.title('Temperature over Time')
        plt.ylabel('Temperature (deg C)')

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=2000)
    plt.show()

def read_from_db(conn, last_timestamp, dev_id):
    ts = None
    temp_time = []
    temp_c = []

    query_str = "SELECT device_address, sensor_type, sensor_value, created_at FROM sensor_data"
    if last_timestamp != None:
        #query_str += "  WHERE created_at > '" + str(last_timestamp) + "'"
        pass
    if dev_id != None:
        query_str = query_str + " WHERE device_address = '"+dev_id+"'"

    query_str = query_str + " ORDER BY created_at"
    query = text(query_str)
    result = conn.execute(query)
    for row in result:
        temp_c.append(float(row[2]))
        #temp_time.append(row[3].strftime('%H:%M:%S'))
        temp_time.append(row[3])
        ts = row[3]

    return temp_c, temp_time, ts

if __name__ == "__main__":
    dev_id = "2"
    conn = connect()
    realtime_plot(conn, dev_id)
    conn.close()
    #read_from_db(None)
