import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime, timezone
from db import connect
from sqlalchemy import text


last_timestamp = None

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    global last_timestamp
    # Read temperature data from the database from last timestamp
    temp_c, temp_time, last_timestamp = read_from_db(last_timestamp)

    # Add x and y to lists
    xs+temp_time
    ys+temp_c

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

def realtime_plot():
    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%H:%M%:S'))
    xs = []
    ys = []

    # Set up plot to call animate() function periodically
    a = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()

def read_from_db(last_timestamp):
    for i in range(2):
        temp_time = []
        temp_c = []
        conn = connect()
        query_str = "SELECT device_address, sensor_type, sensor_value, created_at FROM sensor_data"
        if last_timestamp != None:
            #query_str += " WHERE created_at > '" + last_timestamp.strftime("%Y-%M-%D %H:%M:%S.%f")+"'::timestamp"
            #query_str += " with time zone at time zone '-04' ORDER BY created_at"
            query_str += "  WHERE created_at > '" + str(last_timestamp) + "'"
        else:
            query_str = query_str + " ORDER BY created_at"
        query = text(query_str)
        result = conn.execute(query)
        for row in result:
            temp_c.append(float(row[2]))
            temp_time.append(row[3].strftime('%H:%M:%S'))
        conn.close()
        #return temp_c, temp_time, row[3]
        last_timestamp = row[3]

if __name__ == "__main__":
    #realtime_plot()
    read_from_db(None)
