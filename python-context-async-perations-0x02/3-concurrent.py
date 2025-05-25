import asyncio
import aiosqlite

async def setup_db():
    async with aiosqlite.connect('test.db') as db:
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25), ('Charlie', 35), ('Dave', 45)")
        await db.commit()

async def async_fetch_users():
    async with aiosqlite.connect('test.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        return results

async def async_fetch_older_users():
    async with aiosqlite.connect('test.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        return results

async def fetch_concurrently():
    users, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    print("All users:", users)
    print("Users older than 40:", older_users)

async def main():
    await setup_db()
    await fetch_concurrently()

if __name__ == "__main__":
    asyncio.run(main())
