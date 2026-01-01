from database.db_connection import get_connection


def add_village(name):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO villages (name)
    VALUES (%s)
    """

    cursor.execute(query, (name,))
    conn.commit()
    village_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return village_id


def get_all_villages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM villages ORDER BY name")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_village_by_id(village_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM villages WHERE village_id = %s", (village_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
