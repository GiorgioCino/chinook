from database.DB_connect import DBConnect
from model.dipendente import Dipendente


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
    def getAllDipendenti():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select e.EmployeeId, e.LastName 
            from employee e
                                        """
        cursor.execute(query)

        for row in cursor:
            result.append(Dipendente(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(paese, id_map_dipendente):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct(e.EmployeeId)
from employee e, customer c
where e.EmployeeId = c.SupportRepId 
and c.Country = %s
                                            """
        cursor.execute(query, (paese,))

        for row in cursor:
            result.append(id_map_dipendente[row["EmployeeId"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_fatturato_dipendenti(paesi):
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                select e.EmployeeId, sum(i.total) as fatturato
from employee e, customer c, invoice i
where e.EmployeeId = c.SupportRepId 
and c.Country = %s
and c.CustomerId = i.CustomerId 
group by e.EmployeeId 
            """

        cursor.execute(query, (paesi,))

        for row in cursor:
            result[row["EmployeeId"]] = row["fatturato"]

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_generi_per_dipendente(paese):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT 
            e.EmployeeId,
            t.GenreId
        FROM employee e, customer c, invoice i, invoiceline il, track t
        WHERE e.EmployeeId = c.SupportRepId
          AND c.CustomerId = i.CustomerId
          AND i.InvoiceId = il.InvoiceId
          AND il.TrackId = t.TrackId
          AND c.Country = %s
              
            """

        cursor.execute(query, (paese,))

        for row in cursor:
            result.append((row["EmployeeId"], row["GenreId"]))

        cursor.close()
        conn.close()

        return result

