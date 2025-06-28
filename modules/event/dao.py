from database.connect import ConnectDataBase
from modules.event.event import Event

class EventDao:
    _TABLE_NAME = 'EVENT'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(actor_username, verb_id, object_id, subject_id, result_id)' \
                   ' VALUES (%s, %s, %s, %s, %s) RETURNING id, date_time'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def save(self, event):
        if event.id is None:
            conn = self.database.getconn()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    self._INSERT_INTO,
                    (event.actor_username, event.verb_id, event.object_id, event.subject_id, event.result_id)
                )
                id, date_time = cursor.fetchone()
                conn.commit()
                cursor.close()
                event.id = id
                event.date_time = date_time
                return event
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                self.database.putconn(conn)
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_ALL)
            all_events = cursor.fetchall()
            coluns_name = [desc[0] for desc in cursor.description]
            events = []
            for event_query in all_events:
                data = dict(zip(coluns_name, event_query))
                event = Event(**data)
                events.append(event)
            cursor.close()
            return events
        except Exception as e:
            raise e
        finally:
            self.database.putconn(conn)

    def get_by_id(self, id):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
            coluns_name = [desc[0] for desc in cursor.description]
            event = cursor.fetchone()
            if not event:
                return None
            data = dict(zip(coluns_name, event))
            event = Event(**data)
            cursor.close()
            return event
        except Exception as e:
            raise e
        finally:
            self.database.putconn(conn)

    def delete_event(self, id):
        conn = self.database.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
            conn.commit()
            cursor.close()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.database.putconn(conn)
