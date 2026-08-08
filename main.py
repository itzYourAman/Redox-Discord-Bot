import os
#os.system('pip install -r requirements.txt')
from core.Redox import Redox
import asyncio
client = Redox()

tkn =""
async def main():
  async with client:
    os.system("cls" if os.name == "nt" else "clear")
    await client.load_extension("cogs")
    await client.load_extension("jishaku")
    await client.start(tkn)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass