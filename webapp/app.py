import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/')
def dashboard():
    """Renders the main dashboard page."""
    checks = []
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Query now includes the notification_email to display on the dashboard
            cur.execute("""
                SELECT DISTINCT ON (w.url)
                    w.url,
                    w.notification_email,
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

@app.route('/add', methods=['POST'])
def add_website():
    """Adds a new website and notification email to the database."""
    url = request.form['url']
    email = request.form.get('email')

    if url:
        notification_email = email if email else None
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                # If URL exists, update its email. Otherwise, insert new record.
                cur.execute(
                    "INSERT INTO websites (url, notification_email) VALUES (%s, %s) ON CONFLICT (url) DO UPDATE SET notification_email = EXCLUDED.notification_email;", 
                    (url, notification_email)
                )
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print(f"Database error on insert: {e}")
            
    return redirect(url_for('dashboard'))

@app.route('/delete/<path:url>')
def delete_website(url):
    """Deletes a website from the database."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM websites WHERE url = %s;", (url,))
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        print(f"Database error on delete: {e}")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)