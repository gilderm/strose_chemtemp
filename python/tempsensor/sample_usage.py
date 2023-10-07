# usage.py
# sample usage to sample a pandas DataFrame.
from db import connect
import pandas as pd


sql_query = "select * from pg_catalog.pg_tables pt;"
connection = connect()
dataframe = pd.read_sql(sql_query, connection)

print(dataframe.sample())

connection.close()