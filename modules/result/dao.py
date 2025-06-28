from database.connect import ConnectDataBase
from modules.result.result import Result

class ResultDao:
    _TABLE_NAME = 'RESULT'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(success, response, response_time_seconds) ' \
                   'VALUES (%s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = "SELECT * FROM {} WHERE ID='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def save(self, result):
        if result.id is None:
            conn = self.database.getconn()
            try:
                cursor = conn.cursor()
                cursor.execute(self._INSERT_INTO, (result.success, result.response, result.response_time_seconds))
                id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                result.id = id
                return result
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                self.database.putconn(conn)
        else:
            raise Exception("Erro ao salvar")

    def get_by_id(self, id):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
            row = cursor.fetchone()
            if not row:
                cursor.close()
                return None
            coluns_name = [desc[0] for desc in cursor.description]
            data = dict(zip(coluns_name, row))
            result_obj = Result(**data)
            print("result salvo", result_obj)
            cursor.close()
            return result_obj
        finally:
            self.database.putconn(conn)

    def get_all(self):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_ALL)
            all_results = cursor.fetchall()
            coluns_name = [desc[0] for desc in cursor.description]
            results = []
            for result_query in all_results:
                data = dict(zip(coluns_name, result_query))
                result_obj = Result(**data)
                results.append(result_obj)
            cursor.close()
            return results
        finally:
            self.database.putconn(conn)
