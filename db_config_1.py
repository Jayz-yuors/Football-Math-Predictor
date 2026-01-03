import psycopg2
PG_HOST = "localhost"        # Change to your PG server
PG_PORT = 5432
PG_DB   = "Your DB Name"
PG_USER = "Your DB UserName"      # <-- CHANGE THIS
PG_PASS = "Your DB Password!"  # <-- CHANGE THIS

def create_connection():
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS
    )
    return conn

