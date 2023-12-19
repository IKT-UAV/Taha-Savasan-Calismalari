import psycopg2

db_name="savasan"
db_user="postgres"
db_password="fd49db33b2"
db_host="localhost"
db_port="5432"

conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
cur = conn.cursor()