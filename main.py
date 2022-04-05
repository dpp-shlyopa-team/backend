from os import system
from functions import *
import asyncio
import aiomysql
import re
import json
from send_email import *

loop = asyncio.get_event_loop()

async def main():
  a = json.loads(r"{}")
  print(a.items())
  

loop.run_until_complete(main())

# 292
