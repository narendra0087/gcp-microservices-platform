import os
import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service", version="1.0.0")

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://localhost:8002"
)

PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL",
    "http://localhost:8004"
)

class OrderRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.get("/")
def home():
    return {"service": "order-service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/orders")
async def create_order(order: OrderRequest):

    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:

            # Call Product Service
            product_response = await client.get(
                f"{PRODUCT_SERVICE_URL}/products/{order.product_id}"
            )
            product_response.raise_for_status()
            product = product_response.json()

            amount = product["price"] * order.quantity

            # Call Payment Service
            payment_response = await client.post(
                f"{PAYMENT_SERVICE_URL}/payments",
                json={
                    "order_id": 1001,
                    "amount": amount
                }
            )
            payment_response.raise_for_status()

            payment = payment_response.json()

            return {
                "order_id": 1001,
                "user_id": order.user_id,
                "product": product["name"],
                "quantity": order.quantity,
                "total_amount": amount,
                "payment": payment["status"],
                "payment_id": payment["payment_id"]
            }

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Downstream service returned HTTP {exc.response.status_code}"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="A downstream microservice is unavailable"
        )