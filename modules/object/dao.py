from database.connect import ConnectDataBase
from modules.object.object import Object

class ObjectDao:
    _TABLE_NAME = 'OBJECT'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(id, name_pt, name_en, description_pt, description_en)' \
                   ' VALUES(%s, %s, %s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = "SELECT * FROM {} WHERE ID='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def save(self, object):
        if object.id is not None:
            conn = self.database.getconn()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    self._INSERT_INTO,
                    (object.id, object.name_pt, object.name_en, object.description_pt, object.description_en)
                )
                conn.commit()
                cursor.close()
                return object
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
            object_instance = Object(**data)
            print("object salvo", object_instance)
            cursor.close()
            return object_instance
        finally:
            self.database.putconn(conn)

    def get_all(self):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_ALL)
            all_objects = cursor.fetchall()
            coluns_name = [desc[0] for desc in cursor.description]
            objects = []
            for object_query in all_objects:
                data = dict(zip(coluns_name, object_query))
                object_instance = Object(**data)
                objects.append(object_instance)
            cursor.close()
            return objects
        finally:
            self.database.putconn(conn)
