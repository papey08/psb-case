import psycopg2
from entitties.response import Response
from entitties.tg_user import TgUser

class Repository:
    def __init__(self, db_host, db_port, db_username, db_password, db_database_name):
        try:
            self.connection = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_username,
                password=db_password,
                dbname=db_database_name
            )
            self.connection.autocommit = True
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise
    def get_next_response_in_category(self, category: str, current_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute(Query_Constants.next_category_qwery(category), (current_id,))
            row = cursor.fetchone()
            if row:
                return Response(
                    id=row[2],
                    original_text=row[1],
                    resp_category=category,
                    current_index=row[0]
                )


class Query_Constants:
    @staticmethod
    def next_category_qwery(category: str):
        return f"""
        SELECT c.*
        FROM {category}_v c
        WHERE c.id = %s LIMIT 1
        """