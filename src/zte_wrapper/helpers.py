from datetime import datetime


def utf_16_decode(inp: str) -> str:
    return bytes.fromhex(inp).decode("utf-16-be")


def utf_16_encode(inp: str) -> str:
    return inp.encode("utf-16-be").hex().upper()


def get_zte_timestring(timezone_offset: int) -> str:
    now = datetime.now()

    output = f"{str(now.year)[2:]};{now.month};{now.day};{now.hour+1};{now.minute};{now.second};+{timezone_offset}"

    return output
