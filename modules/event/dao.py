from database.connect import ConnectDataBase
from modules.event.event import Event

class EventDao:
    _TABLE_NAME = 'EVENT'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(actor_username, verb_id, object_id, subject_id, result_id)' \
                   ' values(%s, %s, %s, %s, %s) RETURNING id, date_time'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"


    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def save(self, event):
        if event.id is None:
            cursor = self.database.cursor()
            cursor.execute(self._INSERT_INTO, (event.actor_username, event.verb_id, event.object_id, event.subject_id, event.result_id))
          
            id, date_time = cursor.fetchone()
            self.database.commit()
            cursor.close()
            event.id = id
            event.date_time = date_time
            return event
        else:
            raise Exception('Não é possível salvar')

    def get_all(self):
        events = []
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_ALL)
        all_events = cursor.fetchall()
        print('eventosss', all_events)
        coluns_name = [desc[0] for desc in cursor.description]
        for event_query in all_events:
            data = dict(zip(coluns_name, event_query))
            event = Event(**data)
            events.append(event)
        cursor.close()
        return events

    def get_by_id(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        coluns_name = [desc[0] for desc in cursor.description]
        event = cursor.fetchone()
        if not event:
            return None
        data = dict(zip(coluns_name, event))
        event = Event(**data)
        print(event)
        cursor.close()
        return event

    def delete_event(self, id):
        cursor = self.database.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.database.commit()
        cursor.close()
    
    