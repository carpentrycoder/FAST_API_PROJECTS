from sqlmodel import Session, select
from app.models import User
from app.database import engine

def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()

def get_user(user_id: int):
    with Session(engine) as session:
        return session.get(User, user_id)

def update_user(user_id: int, updated_data: User):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if db_user:
            db_user.name = updated_data.name
            db_user.email = updated_data.email
            db_user.age = updated_data.age
            session.commit()
            session.refresh(db_user)
            return db_user
        return None

def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
