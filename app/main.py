from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, auth
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
print(settings.database_hostname)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Welcome To Auto Glass Pro"}