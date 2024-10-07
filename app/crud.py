from uuid import UUID, uuid4
from typing import Dict, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from . import schemas, models


async def create_product(db: AsyncSession, product_data: schemas.ProductCreate) -> schemas.Product:
    product = models.Product(
        id=uuid4(),
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_products(db: AsyncSession) -> List[schemas.Product]:
    result = await db.execute(select(models.Product))
    products = result.scalars().all()
    return products


async def get_product(db: AsyncSession, id: UUID) -> schemas.Product:
    result = await db.execute(select(models.Product).filter(models.Product.id == id))
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def update_product(db: AsyncSession, id: UUID, product_data: schemas.ProductUpdate) -> schemas.Product:
    product = await get_product(db=db, id=id)

    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, id: UUID) -> schemas.Product:
    product = await get_product(db=db, id=id)
    if product:
        await db.delete(product)
        await db.commit()
    return product


async def create_order(db: AsyncSession, order_data: Dict[UUID, int]) -> schemas.Order:
    try:
        # Create an order with status - "in_progress"
        new_order = models.Order(
            id=uuid4(),
            created_at=datetime.now(),
            status=schemas.OrderStatus.IN_PROGRESS.value)
        db.add(new_order)
        await db.flush()  # Flush to get order ID for order_items

        # Processing of each item in the order
        for product_id, quantity in order_data.items():
            # Availability check
            product = await get_product(db=db, id=product_id)

            if product.quantity < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough quantity for product {product.name}. Requested: {quantity}, Available: {product.quantity}"
                )

            # Create an order item and update the quantity of product in stock
            await create_order_item(db, order_id=new_order.id, product=product, quantity=quantity)

        await db.commit()
        await db.refresh(new_order)

        return new_order

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order due to a database error."
        )


async def get_orders(db: AsyncSession) -> List[schemas.Order]:
    result = await db.execute(select(models.Order))
    orders = result.scalars().all()
    return orders


async def get_order(db: AsyncSession, id: UUID) -> schemas.Order:
    result = await db.execute(select(models.Order).filter(models.Order.id == id))
    order = result.scalars().first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


async def update_order(db: AsyncSession, id: UUID, status: schemas.OrderStatus) -> schemas.Order:
    order = await get_order(db=db, id=id)

    # Update order status to new status
    stmt = update(models.Order).where(models.Order.id == id).values(
        status=status.value
    ).execution_options(synchronize_session="fetch")

    await db.execute(stmt)

    await db.commit()
    await db.refresh(order)

    return order


async def create_order_item(db: AsyncSession, order_id: UUID, product: models.Product, quantity: int) -> schemas.OrderItem:
    # Create order item
    new_order_item = models.OrderItem(
        id=uuid4(),
        order_id=order_id,
        product_id=product.id,
        quantity=quantity
    )
    db.add(new_order_item)

    # Updating the quantity of product in stock
    product.quantity -= quantity

    await db.flush()

    return new_order_item