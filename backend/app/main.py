from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.db.session import engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Influencer Dashboard API")

# Define allowed origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Influencer Dashboard API"} 