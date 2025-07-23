from fastapi import FastAPI
from app import models, database
from app.routes import router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(router, prefix="/friends")
