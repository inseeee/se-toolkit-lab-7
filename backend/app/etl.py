from sqlmodel.ext.asyncio.session import AsyncSession
import httpx
from app.settings import settings
from app.models.item import ItemRecord

async def sync(session: AsyncSession) -> str:
    # Загружаем реальные данные из autochecker API
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.autochecker_api_url}/api/items",
            auth=(settings.autochecker_email, settings.autochecker_password)
        )
        resp.raise_for_status()
        items = resp.json()
    
    for item in items:
        if item['type'] == 'lab':
            existing = await session.exec(
                select(ItemRecord).where(ItemRecord.title == item['title'])
            ).first()
            if not existing:
                lab = ItemRecord(type='lab', title=item['title'])
                session.add(lab)
    
    await session.commit()
    return "ok"
