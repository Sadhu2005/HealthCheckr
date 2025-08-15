import os
import psycopg2
import requests
import time
from psycopg2 import sql

def get_db_connection():
    """Establishes a connection to the database."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "healthchecks"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )

def setup_database(conn):
    """Creates the necessary tables if they don't already exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS websites (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL UNIQUE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS health_checks (
                id SERIAL PRIMARY KEY,
                website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
                checked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                status_code INTEGER,
                response_time_ms INTEGER
            );
        """)
        
        # Add some sample websites if the table is empty
        cur.execute("SELECT COUNT(*) FROM websites;")
        if cur.fetchone()[0] == 0:
            sample_sites = [('https://www.google.com',), ('https://www.github.com',), ('https://sadhujdeveloper.com',)]
            cur.executemany("INSERT INTO websites (url) VALUES (%s) ON CONFLICT (url) DO NOTHING;", sample_sites)

        conn.commit()

def check_websites(conn):
    """Fetches websites and records their health status."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, url FROM websites;")
        websites = cur.fetchall()

        for website_id, url in websites:
            status_code = None
            response_time_ms = -1
            try:
                # Perform the check with a 5-second timeout
                response = requests.get(url, timeout=5)
                status_code = response.status_code
                response_time_ms = int(response.elapsed.total_seconds() * 1000)
            except requests.RequestException as e:
                # Handle timeouts, connection errors, etc.
                print(f"Error checking {url}: {e}")
                status_code = 503  # Service Unavailable

            # Insert the result into the health_checks table
            cur.execute(
                "INSERT INTO health_checks (website_id, status_code, response_time_ms) VALUES (%s, %s, %s);",
                (website_id, status_code, response_time_ms)
            )
            print(f"Checked {url}: Status {status_code}, Response {response_time_ms}ms")
        
        conn.commit()


if __name__ == "__main__":
    print("Starting health checker script...")
    
    # Wait for the database to be ready
    time.sleep(10)

    try:
        conn = get_db_connection()
        setup_database(conn)
        
        # Main loop to check websites periodically
        while True:
            check_websites(conn)
            print("Health check cycle completed. Waiting for 60 seconds...")
            time.sleep(60) # Wait for 60 seconds before the next check

    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()