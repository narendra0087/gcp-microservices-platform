from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI(title="Payment Service", version="1.0.0")

class PaymentRequest(BaseModel):
    order_id: int
    amount: float

@app.get("/")
def home():
    return {"service": "payment-service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/payments")
def process_payment(payment: PaymentRequest):
    return {
        "payment_id": str(uuid4()),
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "SUCCESS"
    }