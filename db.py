import deta
from settings import DATA_KEY


deta_obj = deta.Deta(DATA_KEY)

db_user = deta_obj.Base('user')
db_role = deta_obj.Base('role')


def delete_all_items(db):
    response_data = db.fetch()
    if response_data.count > 0:
        for data in response_data.items:
            db.delete(data['key'])
