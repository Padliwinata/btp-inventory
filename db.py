import deta
from settings import DATA_KEY


deta_obj = deta.Deta(DATA_KEY)

db_role = deta_obj.Base("role")
db_user = deta_obj.Base("user")
db_supplier = deta_obj.Base("supplier")
db_product = deta_obj.Base("product")
db_transaction = deta_obj.Base("transaction")
db_room = deta_obj.Base("room")
db_movement = deta_obj.Base("movement")


drive = deta_obj.Drive("document")


def get_all_db():
    databases = [db_role, db_user, db_supplier, db_product, db_transaction, db_room, db_movement]
    for db in databases:
        yield db


def delete_all_items(db):
    response_data = db.fetch()
    if response_data.count > 0:
        for data in response_data.items:
            db.delete(data['key'])
