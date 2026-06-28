from database.DB_connect import DBConnect
from model.genere import Genere


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                                        select distinct(c.Country)
    from customer c
                                        """
        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct(g.GenreId), g.Name
        from genre g
                                            """
        cursor.execute(query)

        for row in cursor:
            result.append(Genere(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(paese, id_map_genere):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct t.GenreId 
from customer c, invoice i, invoiceline il, track t
where c.Country = %s
and c.CustomerId = i.CustomerId 
and i.InvoiceId = il.InvoiceId 
and il.TrackId = t.TrackId 

                                                """
        cursor.execute(query, (paese,))

        for row in cursor:
            result.append(id_map_genere[row["GenreId"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_edges(paese):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """

                select t.GenreId as g1, t2.GenreId as g2, count(distinct c.CustomerId ) as peso
from customer c, invoice i, invoiceline il, track t, genre g,
customer c2, invoice i2, invoiceline il2, track t2, genre g2
where c.CustomerId = i.CustomerId 
and i.InvoiceId  = il.InvoiceId 
and il.TrackId = t.TrackId 
and t.GenreId = g.GenreId 
and c.CustomerId = i2.CustomerId 
and i2.InvoiceId  = il2.InvoiceId 
and il2.TrackId = t2.TrackId 
and t2.GenreId = g2.GenreId 
and g.GenreId < g2.GenreId 
and c.Country = %s
and c.Country = c2.Country 
group by t.GenreId, t2.GenreId 
                                                """
        cursor.execute(query, (paese,))

        for row in cursor:
            result.append((row["g1"], row["g2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

