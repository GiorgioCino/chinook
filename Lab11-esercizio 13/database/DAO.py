from database.DB_connect import DBConnect
from model.artista import Artista
from model.playlist import Playlist


class DAO():
    @staticmethod
    def getAllPlaylists():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                select distinct(p.Name), p.PlaylistId 
from playlist p
                                """
        cursor.execute(query)

        for row in cursor:
            result.append(Playlist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                    select distinct(a.ArtistId), a.Name 
    from artist a
                                    """
        cursor.execute(query)

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(playlist, id_map_artist):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                        select distinct a.ArtistId 
from playlist p, playlisttrack pt, track t, album a
where p.Name = %s
and p.PlaylistId = pt.PlaylistId 
and pt.TrackId = t.TrackId 
and t.AlbumId = a.AlbumId 

                                        """
        cursor.execute(query, (playlist,))

        for row in cursor:
            result.append(id_map_artist[row["ArtistId"]])

        cursor.close()
        conn.close()
        return result
