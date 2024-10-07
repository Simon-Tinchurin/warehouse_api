from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.sql import func

from .db import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(UUIDType(as_uuid=True), primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUIDType(as_uuid=True), primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False)


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(UUIDType(as_uuid=True), primary_key=True, index=True)
    order_id = Column(UUIDType(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    product_id = Column(UUIDType(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)