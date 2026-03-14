from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.memory import MemorySaver
from psycopg_pool import AsyncConnectionPool
import os
import logging

logger = logging.getLogger(__name__)

async def get_checkpointer():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        try:
            pool = AsyncConnectionPool(
                conninfo=database_url,
                max_size=10,
                kwargs={"autocommit": True, "prepare_threshold": 0},
                open=False,
            )
            await pool.open()
            checkpointer = AsyncPostgresSaver(pool)
            await checkpointer.setup()
            return checkpointer
        except Exception as e:
            logger.warning(f"Failed to connect to database, falling back to in-memory checkpointer: {e}")

    logger.info("Using in-memory checkpointer")
    return MemorySaver()