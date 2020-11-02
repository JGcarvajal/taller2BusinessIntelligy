import psycopg2
# Postgres
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "admin"
PSQL_DB   = "spotifydatawh"

try:
    # Conectarse a la base de datos
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

    # Abrir un cursor para realizar operaciones sobre la base de datos
    cur = conn.cursor()

    # Ejecutar una consulta SELECT
    postgres_insert_query = """ INSERT INTO artista (ID, nombre, popularidad, tipo) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (5, 'Julian', 950,'baca')
    cur.execute(postgres_insert_query, record_to_insert)

    # Obtener los resultados como objetos Python
    conn.commit()

    # Cerrar la conexión con la base de datos
    cur.close()
    conn.close()

    # Recuperar datos del objeto Python


    # Hacer algo con los datos
    print("Ejecutado")

except psycopg2.Error as e:
    print("Error de base de datos: ",e)