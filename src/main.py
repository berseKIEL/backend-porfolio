from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models.porfolio_model import Porfolio
from src.routes.router import router
from src.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_ROUTE}/openapi.json'
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    """
        Inicializar de servicios de base de datos
    """
    db_conn = AsyncIOMotorClient(settings.MONGO_CONNECTION).PorfolioEB
    
    await init_beanie(
        database=db_conn,
        document_models=[Porfolio]
    )
        
app.include_router(router, prefix=settings.API_V1_ROUTE)