import psycopg2


conn = psycopg2.connect("host=localhost user=postgres password=kkkk")
cur = conn.cursor()
cur.execute("CREATE")
