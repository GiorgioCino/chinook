from database.DB_connect import DBConnect
from model.mediatype import MediaType


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
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct(year(i.InvoiceDate)) as anno
from  invoice i

                                                """
        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllMediaTypes():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct m.MediaTypeId, m.Name 
from  mediatype m 


                                                    """
        cursor.execute(query)

        for row in cursor:
            result.append(MediaType(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(id_map_mediatype):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select distinct m.MediaTypeId, m.Name 
    from  mediatype m 


                                                        """
        cursor.execute(query)

        for row in cursor:
            result.append(id_map_mediatype[row["MediaTypeId"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_quantita_vendute(paese, anno):
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                t.MediaTypeId,
                COUNT(DISTINCT il.InvoiceLineId) AS vendite
            FROM customer c, invoice i, invoiceline il, track t
            WHERE c.CustomerId = i.CustomerId 
              AND i.InvoiceId = il.InvoiceId 
              AND il.TrackId = t.TrackId 
              AND c.Country = %s
              AND YEAR(i.InvoiceDate) = %s
            GROUP BY t.MediaTypeId
        """

        cursor.execute(query, (paese, anno))

        for row in cursor:
            result[row["MediaTypeId"]] = row["vendite"]

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_clienti_per_media(paese, anno):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT 
                t.MediaTypeId,
                c.CustomerId,
                MONTH(i.InvoiceDate) AS mese
            FROM customer c, invoice i, invoiceline il, track t
            WHERE c.CustomerId = i.CustomerId 
              AND i.InvoiceId = il.InvoiceId 
              AND il.TrackId = t.TrackId 
              AND c.Country = %s
              AND YEAR(i.InvoiceDate) = %s
        """

        cursor.execute(query, (paese, anno))

        for row in cursor:
            result.append(
                (
                    row["MediaTypeId"],
                    row["CustomerId"],
                    row["mese"]
                )
            )

        cursor.close()
        conn.close()

        return result
