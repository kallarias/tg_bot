from pony.orm import Required, Database, set_sql_debug

from settings import DB_CONFIG

db = Database()
# PostgreSQL
db.bind(**DB_CONFIG)


class UserTasks(db.Entity):
    user_id = Required(int)
    name = Required(str)
    date = Required(str)
    task = Required(str)


db.generate_mapping(create_tables=True)
set_sql_debug(True)
#     UserTasks.get(user_id = 123321)
