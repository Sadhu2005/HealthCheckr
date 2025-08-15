import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the database."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "healthchecks"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )

@app.route('/')
def dashboard():
    """Renders the main dashboard page."""
    checks = []
    try:
        conn = get_db_connection()
        # Use RealDictCursor to get results as dictionaries
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # This query gets the LATEST check for each website
            cur.execute("""
                SELECT DISTINCT ON (w.url)
                    w.url,
                    hc.status_code,
                    hc.response_time_ms,
                    hc.checked_at
                FROM websites w
                LEFT JOIN health_checks hc ON w.id = hc.website_id
                ORDER BY w.url, hc.checked_at DESC;
            """)
            checks = cur.fetchall()
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        # You can pass an error message to the template if you want
        
    return render_template('dashboard.html', checks=checks)

if __name__ == '__main__':
    # '0.0.0.0' makes the app accessible from outside the Docker container
    app.run(host='0.0.0.0', port=5000)