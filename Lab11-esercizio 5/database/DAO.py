from database.DB_connect import DBConnect
from model.genere import Genere
from model.playlist import Playlist


class DAO():
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                select g.Name, g.GenreId
                                from genre g
                                """
        cursor.execute(query)

        for row in cursor:
            result.append(Genere(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPlaylists():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                    select distinct p.PlaylistId, p.Name
                                    from playlist p
                                    """
        cursor.execute(query)

        for row in cursor:
            result.append(Playlist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(genere, id_map_playlist):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                        select distinct(p.PlaylistId)
from playlist p, playlisttrack pt, track t
where p.PlaylistId = pt.PlaylistId 
and pt.TrackId = t.TrackId 
and t.GenreId = %s
                                        """
        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(id_map_playlist[row["PlaylistId"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPopolarita(genere):
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)

        query = """
            select p.PlaylistId, count(distinct(t.trackId)) as peso
from playlist p, playlisttrack pt, track t
where p.PlaylistId = pt.PlaylistId 
and pt.TrackId = t.TrackId 
and t.GenreId = %s
group by p.PlaylistId 
        """

        cursor.execute(query, (genere,))

        for row in cursor:
            result[row["PlaylistId"]] = row["peso"]

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_track_per_playlist(genere):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                        select p.PlaylistId, t.TrackId 
from playlist p, playlisttrack pt, track t
where p.PlaylistId = pt.PlaylistId 
and pt.TrackId = t.TrackId 
and t.GenreId = %s

                    """

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append((row["PlaylistId"], row["TrackId"]))

        cursor.close()
        conn.close()

        return result


