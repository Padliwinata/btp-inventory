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
    key: str
    name: str


class UserDB(BaseModel):
    key: str
    id_role: str
    username: str
    email: str
    passwrd: str


class SupplierDB(BaseModel):
    key: str
    name: str
    phone: str


class ProductDB(BaseModel):
    key: str
    id_supplier: str
    name: str
    description: str
    size: SizeType


class TransactionDB(BaseModel):
    key: str
    id_product: str
    id_user: str
    category: TransactionType
    amount: int
    date: str


class RoomDB(BaseModel):
    key: str
    name: str
    building: str
    number: str
    address: str


class MovementDB(BaseModel):
    key: str
    id_product: str
    id_user: str
    id_room: str
    date: str

