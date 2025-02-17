from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, auth, vehicle, glass, inventory
from .config import settings


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vehicle.router)
app.include_router(glass.router)
app.include_router(inventory.router)


@app.get("/")
def root():
    return {"message": "Welcome To Auto Glass Pro"}