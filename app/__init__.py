from fastapi import FastAPI
from app.models.model import Base, engine
from app.controllers.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Loja PUC-Rio",
    description="API reestruturada no padrão MVC",
    version="1.0.0"
)

app.include_router(router)