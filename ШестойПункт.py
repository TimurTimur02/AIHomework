import psycopg2

db_params = {
    'dbname': 'demo',
    'user': 'postgres',
    'password': 'секрет)',
    'host': 'localhost',
    'port': '5432'
}

try:
    conn = psycopg2.connect(**db_params)

    cur = conn.cursor()

    sql_query = """
    select *
    from seats_view;
    """

    cur.execute(sql_query)

    results = cur.fetchall()

    for row in results:
        print(row)

except psycopg2.Error as e:
    print(f"Ошибка базы данных: {e}")

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
