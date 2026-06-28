from database.DB_connect import DBConnect
from model.composer import Composer
from model.mediatype import MediaType


class DAO():
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
    def get_all_composer():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select t.Composer
                from  track t

                                                """
        cursor.execute(query)

        for row in cursor:
            result.append(row['Composer'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_nodes(mils, media):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    select distinct(t.Composer)
from track t
where t.Composer is not null and t.Composer != ''
and t.Milliseconds >= %s
and t.MediaTypeId = %s


                                                    """
        cursor.execute(query, (mils, media,))

        for row in cursor:
            result.append(Composer(**row))

        cursor.close()
        conn.close()
        return result
