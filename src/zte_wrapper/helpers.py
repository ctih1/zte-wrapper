from datetime import datetime, timedelta


def utf_16_decode(inp: str) -> str:
    return bytes.fromhex(inp).decode("utf-16-be")


def utf_16_encode(inp: str) -> str:
    return inp.encode("utf-16-be").hex().upper()


def get_zte_timestring(timezone_offset: int) -> str:
    now = datetime.now()

    output = f"{str(now.year)[2:]};{now.month};{now.day};{now.hour+1};{now.minute};{now.second};+{timezone_offset}"

    return output


def parse_zte_timestring(string: str) -> datetime:
    year, month, day, hour, minute, second, tz_offset = string.split(";")

    date = datetime(
        int(year), int(month), int(day), int(hour), int(minute), int(second), 0
    )

    date += timedelta(hours=int(tz_offset))

    return date
