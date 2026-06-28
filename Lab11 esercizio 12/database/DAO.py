from database.DB_connect import DBConnect
from model.mediatype import MediaType


class DAO():
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
    def get_all_MediaType():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct(m.MediaTypeId), m.Name
        from  mediatype m

                                        """
        cursor.execute(query)

        for row in cursor:
            result.append(MediaType(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_Nodes(paese, id_map_MediaType):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct (t.MediaTypeId )
from customer c, invoice i, invoiceline il, track t
where c.Country = %s
    and c.CustomerId = i.CustomerId 
    and i.InvoiceId = il.InvoiceId 
    and il.TrackId = t.TrackId 


                                            """
        cursor.execute(query, (paese, ))

        for row in cursor:
            result.append(id_map_MediaType[row["MediaTypeId"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_edges(paese):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """

            SELECT 
    t1.MediaTypeId AS med1,
    t2.MediaTypeId AS med2,
    COUNT(DISTINCT c.CustomerId) AS peso
FROM customer c,
     invoice i1,
     invoiceline il1,
     track t1,
     invoice i2,
     invoiceline il2,
     track t2
WHERE c.CustomerId = i1.CustomerId
  AND i1.InvoiceId = il1.InvoiceId
  AND il1.TrackId = t1.TrackId

  AND c.CustomerId = i2.CustomerId
  AND i2.InvoiceId = il2.InvoiceId
  AND il2.TrackId = t2.TrackId

  AND c.Country = %s
  AND t1.MediaTypeId < t2.MediaTypeId
GROUP BY t1.MediaTypeId, t2.MediaTypeId

                                            """
        cursor.execute(query, (paese,))

        for row in cursor:
            result.append((row["med1"], row["med2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

