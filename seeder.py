from db import db_roles


db_roles.insert_many([
    {'name': 'staff'},
    {'name': 'admin'}
])



