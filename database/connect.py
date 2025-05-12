import psycopg2

class ConnectDataBase:
  def __init__(self):
    self._connect = psycopg2.connect(
      host="ep-delicate-frost-a5pyytjt-pooler.us-east-2.aws.neon.tech",
      database="eduboard",
      user="eduboard_owner",
      password="npg_4Cp1BUurWOak"
    )

  def get_instance(self):
    return self._connect
