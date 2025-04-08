import redis.asyncio as redis
from gateway.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=settings.REDIS_DECODE_RESPONSES
)
