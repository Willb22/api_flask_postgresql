import psycopg2
import os



db_name = 'python_flask_api'
_user = 'postgres'
_passw = os.environ.get('PASSPOSTGRES')
_host = '127.0.0.1'
_port = '5432'

# establishing the connection
conn = psycopg2.connect(
    user=_user, password=_passw, host=_host, port=_port
)
conn.autocommit = True
# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing query to create a database
command = '''CREATE database ''' + db_name;

# Creating a database
cursor.execute(command)
print("Database created successfully........")

# Closing the connection
conn.close()
