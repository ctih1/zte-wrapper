from src.zte_wrapper.wrapper import ZTEWrapper
import asyncio

with open(".password", "r") as f:
    password = f.read()

zte = ZTEWrapper("192.168.32.1", password)


async def main():
    print(await zte.get_signal_strength())


asyncio.run(main())
