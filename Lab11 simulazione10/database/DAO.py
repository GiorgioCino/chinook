from database.DB_connect import DBConnect
from model.genere import Genere


class DAO():
    @staticmethod
    def get_all_genres():
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
    def get_all_countries():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                select distinct(c.Country)
from  customer c

                                """
        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_nodes(genere):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                    
    select distinct(c.Country)
    from track t, invoiceline il, invoice i, customer c
    where t.GenreId = %s
    and t.TrackId = il.TrackId
    and il.InvoiceId = i.InvoiceId
    and i.CustomerId = c.CustomerId

                                    """
        cursor.execute(query,(genere,))

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_edges(genere):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """

        SELECT 
    c1.Country AS paese1,
    c2.Country AS paese2,
    COUNT(DISTINCT a1.ArtistId) AS peso
FROM customer c1,
     invoice i1,
     invoiceline il1,
     track t1,
     mediatype m1,
     customer c2,
     invoice i2,
     invoiceline il2,
     track t2,
     mediatype m2
WHERE c1.CustomerId = i1.CustomerId
  AND i1.InvoiceId = il1.InvoiceId
  AND il1.TrackId = t1.TrackId
  AND t1.AlbumId = a1.AlbumId

  AND c2.CustomerId = i2.CustomerId
  AND i2.InvoiceId = il2.InvoiceId
  AND il2.TrackId = t2.TrackId
  AND t2.AlbumId = a2.AlbumId

  AND t1.GenreId = %s
  AND t1.GenreId = t2.GenreId

  AND a1.ArtistId = a2.ArtistId
  AND c1.Country < c2.Country
GROUP BY c1.Country, c2.Country

                                        """
        cursor.execute(query, (genere,))

        for row in cursor:
            result.append((row["paese1"], row["paese2"], row["peso"]))

        cursor.close()
        conn.close()
        return result


