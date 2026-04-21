import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )

def fetch_rows():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM dbo.encuesta_transporte
    """

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]

    rows = []
    for row in cursor.fetchall():
        rows.append(dict(zip(columns, row)))

    conn.close()
    return rows


def update_codigo(row_id, columna_codigo, valor):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    UPDATE encuesta_transporte  -- ✅ MISMA TABLA
    SET {columna_codigo} = ?
    WHERE id = ?
    """

    cursor.execute(query, valor, row_id)
    conn.commit()
    conn.close()