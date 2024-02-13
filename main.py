import asyncio
from contextlib import asynccontextmanager

from motor import motor_asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deps import DatabaseConnectionMarker
from routers import links

import dotenv
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    dotenv.load_dotenv()
    database = os.getenv(key="MONGO_DATABASE")
    user = os.getenv(key="MONGO_USER")
    password = os.getenv(key="MONGO_PASSWORD")
    cluster = os.getenv(key="MONGO_CLUSTER")

    url = f"mongodb+srv://{user}:{password}@{cluster}.jcdijbc.mongodb.net/{database}?retryWrites=true&w=majority"
    cluster = motor_asyncio.AsyncIOMotorClient(url)
    connection = cluster[database]

    app.dependency_overrides.update(
        {
            DatabaseConnectionMarker: lambda: connection
        }
    )

    yield

    cluster.close()


def register_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    dotenv.load_dotenv()
    app.include_router(links.router, prefix="/links")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("ALLOWED_ORIGINS").split(","),
        allow_credentials=True,
        allow_methods=os.getenv("ALLOWED_METHODS").split(","),
        allow_headers=os.getenv("ALLOWED_HEADERS").split(",")
    )

    return app


def main():
    app = register_app()

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
