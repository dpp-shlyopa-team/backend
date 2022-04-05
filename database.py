# -*- coding: utf-8 -*-
from CONFIG import *

class Database:
  
  def __init__(self) -> None:
    import asyncio
    self.loop = asyncio.get_event_loop()
    
  async def fetchone(self, query: str, args=None) -> tuple:
    import aiomysql
    pool = await aiomysql.create_pool(
      host=config['database']['host'],
      port=config['database']['port'],                         
      user=config['database']['user'],
      password=config['database']['password'],
      db=config['database']['database'],
      loop=self.loop,
      autocommit=True
    )
    
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute(query, args)
        r = await cur.fetchone()
    pool.close()
    await pool.wait_closed()
    return r
  
  async def fetchall(self, query: str, args=None) -> tuple:
    import aiomysql
    pool = await aiomysql.create_pool(
      host=config['database']['host'],
      port=config['database']['port'],                         
      user=config['database']['user'],
      password=config['database']['password'],
      db=config['database']['database'],
      loop=self.loop,
      autocommit=True
    )
    
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute(query, args)
        r = await cur.fetchall()
    pool.close()
    await pool.wait_closed()
    return r
  
  async def execute(self, query: str, args=None) -> int:
    import aiomysql
    pool = await aiomysql.create_pool(
      host=config['database']['host'],
      port=config['database']['port'],                         
      user=config['database']['user'],
      password=config['database']['password'],
      db=config['database']['database'],
      loop=self.loop,
      autocommit=True
    )
    
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute(query, args)
        r = cur.lastrowid
    pool.close()
    await pool.wait_closed()
    return r