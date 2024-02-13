from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from deps import DatabaseConnectionMarker
from services import links

router = APIRouter()


@router.get("/{link}")
async def root(
    link: str,
    connection: AsyncIOMotorDatabase = Depends(DatabaseConnectionMarker)
):
    return await links.shorten_link(link, connection)
