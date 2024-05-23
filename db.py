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
