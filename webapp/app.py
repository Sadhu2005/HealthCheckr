import os
import psycopg2
from psycopg2.extras import RealDictCursor
# Import request, redirect, and url_for for form handling
from flask import Flask, render_template, request, redirect, url_for

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
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
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
        
    return render_template('dashboard.html', checks=checks)

# --- NEW FUNCTION TO HANDLE ADDING WEBSITES ---
@app.route('/add', methods=['POST'])
def add_website():
    """Adds a new website to the database."""
    # Get the URL from the submitted form data
    url = request.form['url']
    if url:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                # Insert the new URL, ignoring duplicates
                cur.execute("INSERT INTO websites (url) VALUES (%s) ON CONFLICT (url) DO NOTHING;", (url,))
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print(f"Database error on insert: {e}")
            
    # Redirect the user back to the main dashboard
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)