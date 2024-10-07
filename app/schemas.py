from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional
import enum


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

    model_config = {
        "from_attributes": True  # Enables ORM objects validation
    }


class Product(ProductCreate):
    id: UUID


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

    model_config = {
        "from_attributes": True
    }


class OrderStatus(str, enum.Enum):
    IN_PROGRESS = 'in_progress'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'


class Order(BaseModel):
    id: UUID
    created_at: datetime
    status: OrderStatus

    model_config = {
        "from_attributes": True
    }

class CreateOrderItem(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int

    model_config = {
        "from_attributes": True
    }

class OrderItem(CreateOrderItem):
    id: UUID

class UpdateOrderStatus(BaseModel):
    status: OrderStatus