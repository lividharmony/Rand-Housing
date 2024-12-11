import asyncio

import asyncpg
from config import DATABASE_URL


async def create_db_pool():
    pool = await asyncpg.create_pool(DATABASE_URL)
    return pool


USER_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100),
    user_id BIGINT UNIQUE,  -- Add UNIQUE constraint here
    user_type VARCHAR(10) CHECK (user_type IN ('student', 'owner'))
);
"""

HOUSING_TABLE = """
CREATE TABLE IF NOT EXISTS housings (
    id SERIAL PRIMARY KEY,
    description TEXT,
    price INTEGER,
    photo VARCHAR(255),
    location TEXT,
    duration INTEGER,
    available BOOLEAN DEFAULT TRUE,
    owner_id BIGINT REFERENCES users(user_id)  -- Now references the unique user_id
);
"""

APPLICATION_TABLE = """
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),  -- References the primary key in users
    housing_id INTEGER REFERENCES housings(id),  -- References the primary key in housings
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected'))
);
"""


async def initialize_database(pool):
    async with pool.acquire() as connection:
        await connection.execute(USER_TABLE)
        await connection.execute(HOUSING_TABLE)
        await connection.execute(APPLICATION_TABLE)
        print("Tables have been created or already exist.")

if __name__ == "__main__":
    asyncio.run(create_db_pool())
