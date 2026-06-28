

from database.DB_connect import DBConnect
from model.artista import Artista
from model.genere import Genere


class DAO():
    @staticmethod
    def get_all_artists():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select *
                    from artist a
                    """
        cursor.execute(query)

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    def get_all_genres():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                            select g.Name
                            from genre g
                            """
        cursor.execute(query)

        for row in cursor:
            result.append(Genere(**row))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_nodes(genere_id, id_map_artists):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT a.ArtistId
            FROM artist a, album al, track t
            WHERE a.ArtistId = al.ArtistId
              AND al.AlbumId = t.AlbumId
              AND t.GenreId = %s
        """

        cursor.execute(query, (genere_id,))

        for row in cursor:

            result.append(id_map_artists[row["ArtistId"]])

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_popolarita_artisti(genere_id):
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT al.ArtistId, SUM(il.Quantity) AS popolarita
            FROM invoiceline il, track t, album al
            WHERE il.TrackId = t.TrackId
              AND t.AlbumId = al.AlbumId
              AND t.GenreId = %s
            GROUP BY al.ArtistId
        """

        cursor.execute(query, (genere_id,))

        for row in cursor:
            result[row["ArtistId"]] = row["popolarita"]

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_artisti_per_cliente(genere_id):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT i.CustomerId, al.ArtistId
            FROM invoice i, invoiceline il, track t, album al
            WHERE i.InvoiceId = il.InvoiceId
              AND il.TrackId = t.TrackId
              AND t.AlbumId = al.AlbumId
              AND t.GenreId = %s
        """

        cursor.execute(query, (genere_id,))

        for row in cursor:
            result.append((row["CustomerId"], row["ArtistId"]))

        cursor.close()
        conn.close()

        return result