from fastapi import FastAPI
from app.api.routes import auth, user
from app.db.database import Base, engine
from app.db.seed import seed

app = FastAPI()

Base.metadata.create_all(bind=engine)
seed()

app.include_router(auth.router)
app.include_router(user.router)
