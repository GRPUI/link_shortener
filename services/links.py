from typing import List, Dict, Any
import string
import random

from motor import motor_asyncio


async def shorten_link(link: str, connection: motor_asyncio.AsyncIOMotorDatabase) -> Dict[str, Any]:
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))

    _id = await connection.links.count_documents({})

    if await connection.links.count_documents({"link": link}) > 0:
        return None

    await connection.links.insert_one(
        {"_id": _id, "link": link, "_shortened_link": f"coshorty.work.gd/{random_string}"})
    return {"shortened_link": random_string}
