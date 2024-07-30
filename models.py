from enum import Enum
from pydantic import BaseModel


class SizeType(Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'


class TransactionType(Enum):
    IN = 'IN'
    OUT = 'OUT'


class RoleDB(BaseModel):
    data_key: str
    name: str


class UserDB(BaseModel):
    data_key: str
    id_role: str
    username: str
    email: str
    is_active: bool
    password: str


class SupplierDB(BaseModel):
    data_key: str
    name: str
    phone: str


class ProductDB(BaseModel):
    data_key: str
    id_supplier: str
    name: str
    description: str
    size: SizeType


class TransactionDB(BaseModel):
    data_key: str
    id_product: str
    id_user: str
    category: TransactionType
    amount: int
    date: str


class RoomDB(BaseModel):
    data_key: str
    name: str
    building: str
    number: str
    address: str


class MovementDB(BaseModel):
    data_key: str
    id_product: str
    id_user: str
    id_room: str
    date: str

