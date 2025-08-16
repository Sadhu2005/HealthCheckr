import os
import psycopg2
import requests
import time
import smtplib
from email.message import EmailMessage
import os
import psycopg2
import dj_database_url

def get_db_connection():
    """Establishes a connection to the database."""
    # Check for Render's DATABASE_URL first
    if 'DATABASE_URL' in os.environ:
        conn_params = dj_database_url.parse(os.environ['DATABASE_URL'])
        return psycopg2.connect(**conn_params)
    else:
        # Fallback to our local Docker setup
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "healthchecks"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password")
        )

def column_exists(cur, table_name, column_name):
    """Checks if a column exists in a table."""
    cur.execute("""
        SELECT 1 FROM information_schema.columns 
        WHERE table_name=%s AND column_name=%s
    """, (table_name, column_name))
    return cur.fetchone() is not None

def setup_database(conn):
    """Creates/updates tables."""
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
        if not column_exists(cur, 'websites', 'notification_email'):
            cur.execute("ALTER TABLE websites ADD COLUMN notification_email TEXT;")
        if not column_exists(cur, 'websites', 'last_status_code'):
            cur.execute("ALTER TABLE websites ADD COLUMN last_status_code INTEGER;")
        conn.commit()

def send_email_alert(recipient, url, status):
    """Sends an email alert using SMTP credentials from environment variables."""
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not all([sender_email, password, smtp_server, smtp_port]):
        print("SMTP environment variables not set. Skipping email.")
        return

    msg = EmailMessage()
    if status == "DOWN":
        msg['Subject'] = f"🚨 Website Down: {url}"
        msg.set_content(f"The website {url} is currently down or returning an error.")
    elif status == "UP":
        msg['Subject'] = f"✅ Website Up: {url}"
        msg.set_content(f"The website {url} has recovered and is now back online.")

    msg['From'] = sender_email
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"Alert email sent to {recipient} for {url}.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def check_websites(conn):
    """Fetches websites, records their health, and sends alerts on status change."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, url, notification_email, last_status_code FROM websites;")
        websites = cur.fetchall()

        for website_id, url, email, last_status in websites:
            status_code = None
            response_time_ms = -1
            try:
                response = requests.get(url, timeout=5)
                status_code = response.status_code
                response_time_ms = int(response.elapsed.total_seconds() * 1000)
            except requests.RequestException:
                status_code = 503

            cur.execute(
                "INSERT INTO health_checks (website_id, status_code, response_time_ms) VALUES (%s, %s, %s);",
                (website_id, status_code, response_time_ms)
            )
            
            if status_code != last_status:
                cur.execute(
                    "UPDATE websites SET last_status_code = %s WHERE id = %s;",
                    (status_code, website_id)
                )
                print(f"Status changed for {url} from {last_status} to {status_code}.")
                if email:
                    # --- THIS IS THE CORRECTED LOGIC ---
                    if status_code != 200 and (last_status == 200 or last_status is None):
                        send_email_alert(email, url, "DOWN")
                    elif status_code == 200 and last_status is not None and last_status != 200:
                        send_email_alert(email, url, "UP")
            
            print(f"Checked {url}: Status {status_code}, Response {response_time_ms}ms")
        conn.commit()


if __name__ == "__main__":
    print("Starting health checker script with email capability...")
    time.sleep(10)
    try:
        conn = get_db_connection()
        setup_database(conn)
        while True:
            check_websites(conn)
            print("Health check cycle completed. Waiting for 60 seconds...")
            time.sleep(60)
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()