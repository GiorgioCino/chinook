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
                                                select distinct (t.GenreId )
from customer c, invoice i, invoiceline il, track t
where c.CustomerId = i.CustomerId 
and i.InvoiceId = il.InvoiceId 
and il.TrackId = t.TrackId 
and c.Country = %s
                                                """
        cursor.execute(query, (paese,))

        for row in cursor:
            result.append(id_map_genere[row["GenreId"]])

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def get_clienti_per_genere(paese):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT 
                t.GenreId,
                c.CustomerId
            FROM customer c, invoice i, invoiceline il, track t
            WHERE c.CustomerId = i.CustomerId 
              AND i.InvoiceId = il.InvoiceId 
              AND il.TrackId = t.TrackId 
              AND c.Country = %s
        """

        cursor.execute(query, (paese,))

        for row in cursor:
            result.append(
                (
                    row["GenreId"],
                    row["CustomerId"]

                )
            )

        cursor.close()
        conn.close()

        return result



