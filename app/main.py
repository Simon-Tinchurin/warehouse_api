import logging
from uuid import UUID
from typing import List, Dict

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.crud as crud
import app.schemas as schemas
import app.db as database

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="Warehouse API",
    description="Warehouse API for order management",
    version="1.0.0",
    docs_url="/docs",  # URL for Swagger UI
    redoc_url="/redoc",  # URL for ReDoc
    )

# Endpoints for products:

# Create a product (POST /products).
@app.post("/products", response_model=schemas.Product, summary="Create a new product", tags=["Products"])
async def create_product(product_data: schemas.ProductCreate, db: AsyncSession = Depends(database.get_db)):
    """
    Create a new product in the warehouse.
    
    Args:
        product_data (schemas.ProductCreate): Product information to be created.
    
    Returns:
        schemas.Product: The newly created product.
    """
    return await crud.create_product(db=db, product_data=product_data)


# Get a list of all products (GET /products).
@app.get("/products", response_model=List[schemas.Product], summary="Get list of all products", tags=["Products"])
async def get_products(db: AsyncSession = Depends(database.get_db)):
    """
    Retrieve a list of all products available in the warehouse.
    
    Returns:
        List[schemas.Product]: A list of all products.
    """
    return await crud.get_products(db=db)


# Get product details by ID (GET /products/{id}).
@app.get("/products/{id}", response_model=schemas.Product, summary="Get product by ID", tags=["Products"])
async def get_product(id: UUID, db: AsyncSession = Depends(database.get_db)):
    """
    Retrieve details of a product by its ID.
    
    Args:
        id (UUID): The unique identifier of the product.
    
    Returns:
        schemas.Product: The product details.
    """
    return await crud.get_product(db=db, id=id)


# Update product information (PUT /products/{id}).
@app.put("/products/{id}", response_model=schemas.Product, summary="Update product data by ID", tags=["Products"])
async def update_product(id: UUID, product_data: schemas.ProductUpdate, db: AsyncSession = Depends(database.get_db)):
    """
    Update the information of an existing product by its ID.
    
    Args:
        id (UUID): The unique identifier of the product to update.
        product_data (schemas.ProductUpdate): The updated product information.
    
    Returns:
        schemas.Product: The updated product.
    """
    return await crud.update_product(db=db, id=id, product_data=product_data)


# Delete a product (DELETE /products/{id}).
@app.delete("/products/{id}", response_model=schemas.Product, summary="Delete product by ID", tags=["Products"])
async def delete_product(id: UUID, db: AsyncSession = Depends(database.get_db)):
    """
    Delete an existing product by its ID.
    
    Args:
        id (UUID): The unique identifier of the product to delete.
    
    Returns:
        schemas.Product: The deleted product.
    """
    return await crud.delete_product(db=db, id=id)


# Endpoints for orders:

# Create an order (POST /orders).
@app.post("/orders", response_model=schemas.Order, summary="Create a new order", tags=["Orders"])
async def create_order(order_data: Dict[UUID, int], db: AsyncSession = Depends(database.get_db)):
    """
    Create a new order with a list of products and their quantities.
    
    Args:
        order_data (Dict[UUID, int]): A dictionary of product IDs and their respective quantities.
    
    Returns:
        schemas.Order: The newly created order.
    """
    return await crud.create_order(db=db, order_data=order_data)


# Get a list of all orders (GET /orders).
@app.get("/orders", response_model=List[schemas.Order], summary="Get list of all orders", tags=["Orders"])
async def get_orders(db: AsyncSession = Depends(database.get_db)):
    """
    Retrieve a list of all orders.
    
    Returns:
        List[schemas.Order]: A list of all orders.
    """
    return await crud.get_orders(db=db)


# Get order details by ID (GET /orders/{id}).
@app.get("/orders/{id}", response_model=schemas.Order, summary="Get order by ID", tags=["Orders"])
async def get_order(id: UUID, db: AsyncSession = Depends(database.get_db)):
    """
    Retrieve details of an order by its ID.
    
    Args:
        id (UUID): The unique identifier of the order.
    
    Returns:
        schemas.Order: The order details.
    """
    return await crud.get_order(db=db, id=id)


# Update order status (PATCH /orders/{id}/status).
@app.patch("/orders/{id}/status", response_model=schemas.Order, summary="Update order status", tags=["Orders"])
async def update_order(id: UUID, update_data: schemas.UpdateOrderStatus, db: AsyncSession = Depends(database.get_db)):
    """
    Update the status of an existing order by its ID.
    
    Args:
        id (UUID): The unique identifier of the order to update.
        update_data (schemas.UpdateOrderStatus): The new status for the order.
    
    Returns:
        schemas.Order: The updated order with the new status.
    """
    return await crud.update_order(db=db, id=id, status=update_data.status)
