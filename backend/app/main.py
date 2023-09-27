from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .db.sqlite_database import setup_schema
from .routers import authentication, properties, users
from .shared.token import invalid_token

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
PREFIX = "/api/v0"

setup_schema()


def verify_token(x_token: str = Header()):
    if invalid_token(x_token):
        raise HTTPException(status_code=401, detail="User is unauthorized")


app.include_router(authentication.router, prefix=PREFIX,
                   tags=["auth"],
                   dependencies=[],
                   )
app.include_router(properties.router, prefix=PREFIX,
                   tags=["properties"],
                   dependencies=[Depends(verify_token)],
                   )
app.include_router(users.router, prefix=f"{PREFIX}/users",
                   tags=["users"],
                   dependencies=[Depends(verify_token)],
                   )
