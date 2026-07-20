from pathlib import Path
import sqlite3
import os

DB_PATH = Path(os.environ.get('DB_PATH', Path(__file__).parent / 'clients.db'))


class Client:
    def __init__(self, name, street, city_state_zip, email='', cc_emails=''):
        self.name = name
        self.street = street
        self.city_state_zip = city_state_zip
        self.email = email or ''
        self.cc_emails = cc_emails or ''


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS clients (
                name TEXT,
                street TEXT,
                statezip TEXT,
                email TEXT
            );
            CREATE TABLE IF NOT EXISTS business_info (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS invoice_counter (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                value INTEGER NOT NULL
            );
        ''')
        cols = [r[1] for r in conn.execute('PRAGMA table_info(clients)').fetchall()]
        if 'email' not in cols:
            conn.execute('ALTER TABLE clients ADD COLUMN email TEXT')
        if 'cc_emails' not in cols:
            conn.execute('ALTER TABLE clients ADD COLUMN cc_emails TEXT')


def get_clients():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            'SELECT name, street, statezip, email, cc_emails FROM clients ORDER BY name'
        ).fetchall()
    return [Client(r[0], r[1], r[2], r[3], r[4]) for r in rows]


def get_client_email(name):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute('SELECT email FROM clients WHERE name = ?', (name,)).fetchone()
    return row[0] if row and row[0] else None


def get_client_cc_emails(name):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute('SELECT cc_emails FROM clients WHERE name = ?', (name,)).fetchone()
    if not row or not row[0]:
        return []
    return [e.strip() for e in row[0].split(',') if e.strip()]


def update_client(original_name, name, street, city_state_zip, email='', cc_emails=''):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            'UPDATE clients SET name=?, street=?, statezip=?, email=?, cc_emails=? WHERE name=?',
            (name, street, city_state_zip, email or None, cc_emails or None, original_name)
        )


def delete_client(name):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM clients WHERE name=?', (name,))


def add_client(name, street, city_state_zip, email='', cc_emails=''):
    with sqlite3.connect(DB_PATH) as conn:
        exists = conn.execute('SELECT 1 FROM clients WHERE name = ?', (name,)).fetchone()
        if not exists:
            conn.execute(
                'INSERT INTO clients (name, street, statezip, email, cc_emails) VALUES (?, ?, ?, ?, ?)',
                (name, street, city_state_zip, email or None, cc_emails or None)
            )


def load_business_info():
    with sqlite3.connect(DB_PATH) as conn:
        rows = dict(conn.execute('SELECT key, value FROM business_info').fetchall())
    if all(k in rows for k in ('company', 'street', 'phone')):
        return rows
    return None


def save_business_info(company, street, phone):
    with sqlite3.connect(DB_PATH) as conn:
        for key, value in [('company', company), ('street', street), ('phone', phone)]:
            conn.execute('INSERT OR REPLACE INTO business_info (key, value) VALUES (?, ?)',
                         (key, value))


def load_invoice_counter():
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute('SELECT value FROM invoice_counter WHERE id = 1').fetchone()
    return str(row[0]) if row else '1'


def set_invoice_counter(value):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT OR REPLACE INTO invoice_counter (id, value) VALUES (1, ?)',
                     (int(value),))


def increment_invoice_counter():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('UPDATE invoice_counter SET value = value + 1 WHERE id = 1')
