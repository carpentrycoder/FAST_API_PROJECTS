from fastapi import FastAPI, HTTPException
from app.models import User, UserCreate
from app.database import create_db_and_tables
from app.crud import create_user, get_users, get_user, update_user, delete_user

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ✅ POST: Create new user
@app.post("/users_post", response_model=User)
def api_create_user(user: UserCreate):
    return create_user(User.from_orm(user))


# ✅ GET: All users
@app.get("/users_get", response_model=list[User])
def api_get_users():
    return get_users()


# ✅ GET: One user by ID
@app.get("/users/{user_id}", response_model=User)
def api_get_user(user_id: int):
    user = get_user(user_id)
    if not user:  # ⛔ "If" → "if"
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ✅ PUT: Update user
@app.put("/users/{user_id}", response_model=User)
def api_update_user(user_id: int, user: User):
    updated = update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


# ✅ DELETE: Delete user
@app.delete("/users/{user_id}")
def api_delete_user(user_id: int):
    success = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
