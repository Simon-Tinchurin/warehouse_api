import pytest


@pytest.mark.asyncio
async def test_create_product(async_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 50
    }
    response = await async_client.post("/products", json=product_data)
    assert response.status_code == 200, f"Response text: {response.text}"
    assert response.json()["name"] == "Test Product"
    assert response.json()["description"] == "Test Description"
    assert response.json()["price"] == 100.0
    assert response.json()["quantity"] == 50


@pytest.mark.asyncio
async def test_get_products(async_client):
    response = await async_client.get("/products")
    assert response.status_code == 200, f"Response text: {response.text}"
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_product_by_id(async_client):
    # Create a product to get its ID
    product_data = {
        "name": "Test Product Get",
        "description": "Test Description Get",
        "price": 150.0,
        "quantity": 30
    }
    create_response = await async_client.post("/products", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # Get product by ID
    response = await async_client.get(f"/products/{product_id}")
    assert response.status_code == 200, f"Response text: {response.text}"
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Test Product Get"


@pytest.mark.asyncio
async def test_update_product(async_client):
    # Create a product to update
    product_data = {
        "name": "Product to Update",
        "description": "Original Description",
        "price": 200.0,
        "quantity": 20
    }
    create_response = await async_client.post("/products", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # Update product
    updated_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 250.0,
        "quantity": 15
    }
    update_response = await async_client.put(f"/products/{product_id}", json=updated_data)
    assert update_response.status_code == 200, f"Response text: {update_response.text}"
    assert update_response.json()["name"] == "Updated Product"
    assert update_response.json()["description"] == "Updated Description"


@pytest.mark.asyncio
async def test_delete_product(async_client):
    # Create a product to delete
    product_data = {
        "name": "Product to Delete",
        "description": "To be deleted",
        "price": 50.0,
        "quantity": 10
    }
    create_response = await async_client.post("/products", json=product_data)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # Delete product
    delete_response = await async_client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200, f"Response text: {delete_response.text}"
    assert delete_response.json()["id"] == product_id


@pytest.mark.asyncio
async def test_create_order(async_client):
    # Create a product to add to the order
    product_data = {
        "name": "Order Product",
        "description": "For order",
        "price": 100.0,
        "quantity": 100
    }
    create_product_response = await async_client.post("/products", json=product_data)
    assert create_product_response.status_code == 200
    product_id = create_product_response.json()["id"]

    # Create an order
    order_data = {product_id: 2}
    create_order_response = await async_client.post("/orders", json=order_data)
    assert create_order_response.status_code == 200, f"Response text: {create_order_response.text}"
    assert create_order_response.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_get_orders(async_client):
    # Get list of all orders
    response = await async_client.get("/orders")
    assert response.status_code == 200, f"Response text: {response.text}"
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_order_by_id(async_client):
    # Create a product and an order
    product_data = {
        "name": "Order Product Get",
        "description": "For order get",
        "price": 100.0,
        "quantity": 50
    }
    create_product_response = await async_client.post("/products", json=product_data)
    assert create_product_response.status_code == 200
    product_id = create_product_response.json()["id"]

    order_data = {product_id: 1}
    create_order_response = await async_client.post("/orders", json=order_data)
    assert create_order_response.status_code == 200
    order_id = create_order_response.json()["id"]

    # Get order by ID
    response = await async_client.get(f"/orders/{order_id}")
    assert response.status_code == 200, f"Response text: {response.text}"
    assert response.json()["id"] == order_id


@pytest.mark.asyncio
async def test_update_order_status(async_client):
    # Create a product and an order
    product_data = {
        "name": "Order Product Update",
        "description": "For order update",
        "price": 100.0,
        "quantity": 50
    }
    create_product_response = await async_client.post("/products", json=product_data)
    assert create_product_response.status_code == 200
    product_id = create_product_response.json()["id"]

    order_data = {product_id: 1}
    create_order_response = await async_client.post("/orders", json=order_data)
    assert create_order_response.status_code == 200
    order_id = create_order_response.json()["id"]

    # Update order status
    updated_status = {"status": "shipped"}
    update_response = await async_client.patch(f"/orders/{order_id}/status", json=updated_status)
    assert update_response.status_code == 200, f"Response text: {update_response.text}"
    assert update_response.json()["status"] == "shipped"
