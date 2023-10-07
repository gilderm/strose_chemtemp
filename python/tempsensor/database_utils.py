import psycopg2

class DatabaseUtils(object):
   def __init__(self, host, database, user, password):
       self.conn = self.__connect_to_db(host, database, user, password)


   def __connect_to_db(self, host, db, user, password):
      conn = psycopg2.connect(
               host=host,
               database=db,
               user=user,
               password=password,
               port='5432',
               options="-c search_path=chemtemp")
      return conn


