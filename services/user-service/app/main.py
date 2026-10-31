from fastapi import FastAPI, HTTPException

app = FastAPI(title="User Service", version="1.0.0")

users = {
    1: {"id": 1, "name": "Narendra", "email": "narendra@example.com"}
}

@app.get("/")
def home():
    return {"service": "user-service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/users")
def get_users():
    return list(users.values())

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
def create_user(user: dict):
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {
        "id": user_id,
        "name": user["name"],
        "email": user["email"]
    }
    return users[user_id]