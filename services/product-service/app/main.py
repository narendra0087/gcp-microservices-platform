from fastapi import FastAPI, HTTPException

app = FastAPI(title="Product Service", version="1.0.0")

products = {
    101: {"id": 101, "name": "Laptop", "price": 75000},
    102: {"id": 102, "name": "Mobile", "price": 25000},
    103: {"id": 103, "name": "Keyboard", "price": 1500}
}

@app.get("/")
def home():
    return {"service": "product-service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/products")
def get_products():
    return list(products.values())

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product