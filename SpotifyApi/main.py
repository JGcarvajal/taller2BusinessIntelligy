
import pandas as pd
import spotipy
import psycopg2
import io
import dateutil

# Nos conectamos a spotyfy con las credenciales https://beta.developer.spotify.com/
sp = spotipy.Spotify()
from spotipy.oauth2 import SpotifyClientCredentials

import datetime,time

#se obtiene la fecha en formato unix
dts = datetime.datetime.utcnow()
fechaunix = round(time.mktime(dts.timetuple()) + dts.microsecond/1e6)

#creamos las variables de conexion a la DB
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "admin"
PSQL_DB   = "spotifydatawh"

#Creamod las variables de acceso al api de spotify
cid = "9edaff9c2429471cafb87ad184e8aed7"
secret = "f9ed44ee83564264b38d1e3006f20a43"

#creamos la conexion a spotify
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

#Consultamos la lista de artistas
req_artist = sp.artists(["2ye2Wgw4gimLv2eAKyk1NB","16oZKvXb6WkQlVAjwo2Wbg","5M52tdBnJaKSvOpJGz8mfZ","36QJpDe2go2KgaRleHCDTp",
                         "1zng9JZpblpk48IPceRWs8","74ASZWbe4lXaubB36ztrGX","3fMbdgg4jU18AjLCKBhRSm"])


#variables para almacenar los objetos
ids = []
song = []
artist = []

#iteramos los artistas
for i in range(len(req_artist["artists"])):
    art = req_artist["artists"][i]
    artist.append([art["name"], art["popularity"], art["type"], art["uri"], art["followers"]["total"],
               fechaunix, "api", art["id"]])

    #consultamos las canciones de cada artista
    tracks = sp.artist_top_tracks(art["id"])
    songs = tracks["tracks"]

    #iteramos las canciones
    for i in range(len(songs)):
        s = songs[i]
        ids.append(s["id"])
        fecha = dateutil.parser.parse(s["album"]["release_date"])
        fecha2 = fecha.strftime('%Y / $m / %d')
        song.append(
            [s["name"], s["type"], s["artists"][0]["id"], s["album"]["name"],s["track_number"],s["popularity"],s["id"],s["uri"],
             fecha, "", fechaunix,"api"])

#pasamos los artistas a un DataFrame
dataArtists = pd.DataFrame(artist)

#pasamos las canciones a un DataFrame
dataSongs = pd.DataFrame(song)

try:
    # Conectarse a la base de datos
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

    # Abrir un cursor para realizar operaciones sobre la base de datos
    cur = conn.cursor()

    #Copiamos los datafremes a las tabla de Base de Datos
    ouArtist = io.StringIO()
    dataArtists.to_csv(ouArtist, sep='\t', header=False, index=False)
    ouArtist.seek(0)
    contents = ouArtist.getvalue()
    cur.copy_from(ouArtist, 'artista', null="")  # null values become ''

    ouSongs = io.StringIO()
    dataSongs.to_csv(ouSongs, sep='\t', header=False, index=False)
    ouSongs.seek(0)
    contents2 = ouSongs.getvalue()
    cur.copy_from(ouSongs, 'cancion', null="")  # null values become ''

    #Hacemos commit de la transaccion
    conn.commit()

    # Cerrar la conexión con la base de datos
    cur.close()
    conn.close()

    # Confirmamos la ejecusion
    print("Ejecutado")

except psycopg2.Error as e:
    print("Error de base de datos: ",e)
