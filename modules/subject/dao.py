from database.connect import ConnectDataBase
from modules.subject.subject import Subject

class SubjectDao:
    _TABLE_NAME = 'SUBJECT'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(name_pt, name_en, description_pt, description_en)' \
                   ' VALUES(%s, %s, %s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_NAME_PT = "SELECT * FROM {} WHERE NAME_PT='{}'"
    _SELECT_BY_ID = "SELECT * FROM {} WHERE ID='{}'"
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def save(self, subject):
        if subject.id is None:
            conn = self.database.getconn()
            try:
                cursor = conn.cursor()
                cursor.execute(self._INSERT_INTO, (
                    subject.name_pt,
                    subject.name_en,
                    subject.description_pt,
                    subject.description_en
                ))
                subject.id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                return subject
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                self.database.putconn(conn)
        else:
            raise Exception("Erro ao salvar")

    def get_by_name_pt(self, name_pt):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BY_NAME_PT.format(self._TABLE_NAME, name_pt))
            subject = cursor.fetchone()
            if not subject:
                cursor.close()
                return None
            coluns_name = [desc[0] for desc in cursor.description]
            data = dict(zip(coluns_name, subject))
            subject_obj = Subject(**data)
            cursor.close()
            return subject_obj
        finally:
            self.database.putconn(conn)

    def get_by_id(self, id):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
            subject = cursor.fetchone()
            if not subject:
                cursor.close()
                return None
            coluns_name = [desc[0] for desc in cursor.description]
            data = dict(zip(coluns_name, subject))
            subject_obj = Subject(**data)
            cursor.close()
            return subject_obj
        finally:
            self.database.putconn(conn)

    def get_all(self):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_ALL)
            all_subjects = cursor.fetchall()
            coluns_name = [desc[0] for desc in cursor.description]
            subjects = []
            for subject_query in all_subjects:
                data = dict(zip(coluns_name, subject_query))
                subject = Subject(**data)
                subjects.append(subject)
            cursor.close()
            return subjects
        finally:
            self.database.putconn(conn)
