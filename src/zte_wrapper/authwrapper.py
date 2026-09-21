import logging
import aiohttp
from hashlib import sha256
import urllib.parse
import time
import json
from typing import Literal, Dict, Any, Tuple
from copy import deepcopy

logger = logging.getLogger("zte")

GOFORM_COMMANDS = Literal["goform_get_cmd_process", "goform_set_cmd_process"]
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "192.168.32.1",
    "Referer": "http://192.168.32.1/",
    "Sec-Gpc": "1",
    "User-Agent": "Mozilla",
    "X-Requested-With": "XMLHttpRequest",
}


def zte_sha256_string(input: str) -> str:
    return sha256(input.encode("UTF-8")).hexdigest().upper()


class ZTEAuthWrapper:
    def __init__(self, webui_address: str, password: str) -> None:
        self.address: str = webui_address
        self.__password = zte_sha256_string(password)
        self.__auth_code: str | None = None

        self.headers = HEADERS
        self.headers["Referer"] = f"http://{self.address}/"
        self.headers["Host"] = self.address

        self.session: aiohttp.ClientSession | None = None

    def construct_url(self, command: GOFORM_COMMANDS, args: Dict[str, Any]) -> str:
        base_url = f"http://{self.address}/goform/{command}/?"

        url = base_url + urllib.parse.urlencode(
            {k: urllib.parse.quote(str(v)) for k, v in args.items()}
        )

        logger.debug(f"Constructed url {url}")
        return url

    def get_timestamp(self) -> int:
        return round(time.time() * 1000)

    async def __get_ld(self) -> str:
        async with aiohttp.ClientSession() as session:
            res = await session.get(
                self.construct_url(
                    "goform_get_cmd_process",
                    {"isTest": "false", "cmd": "LD", "_": self.get_timestamp()},
                ),
                headers=self.headers,
            )

            logger.info("Got LD token")
            return json.loads((await res.text())).get(
                "LD"
            )  # json.loads instead of res.json() because the stupid API returns the stuff as text/html

    async def __get_rd0_rd1(self) -> Tuple[str, str]:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "cr_version,wa_inner_version",
                    "multi_data": "1",
                },
            ),
        )
        res_text = await res.text()
        logger.debug(f"Retrieved rd0 and rd1: {res_text}")

        data = json.loads(res_text)
        return (data["wa_inner_version"], data["cr_version"])

    async def __get_rd_token(self) -> str:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {"isTest": "false", "cmd": "RD", "_": self.get_timestamp()},
            ),
        )
        logger.debug("")
        return json.loads(await res.text())["RD"]

    # please check notes/tokens.md if it breaks, it might help you a little
    async def construct_ad_token(self) -> str:
        rd0, rd1 = await self.__get_rd0_rd1()
        first_step = zte_sha256_string(rd0 + rd1)
        rd_token = await self.__get_rd_token()
        return zte_sha256_string(first_step + rd_token)

    async def refresh_auth(self) -> str:
        ld_token: str = await self.__get_ld()
        hashed_password: str = zte_sha256_string(self.__password + ld_token)

        async with aiohttp.ClientSession() as session:
            logger.debug("Refreshing authentication")
            res = await session.post(
                self.construct_url("goform_set_cmd_process", {}),
                data={
                    "isTest": "false",
                    "goformId": "LOGIN",
                    "password": hashed_password,
                },
                headers=self.headers,
            )
            self.__auth_code = str(res.cookies.get("stok"))

        return self.__auth_code

    async def confirm_auth(self) -> bool:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {"isTest": "false", "cmd": "date_month", "_": self.get_timestamp()},
            ),
            skip_auth_check=True,
        )

        result = bool(json.loads(await res.text())["date_month"])
        logger.debug(f"Logged in? {result}")

        return result

    async def request(
        self, method: Literal["GET", "POST"], *args, **kwargs
    ) -> aiohttp.ClientResponse:
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = deepcopy(self.headers)
        headers["Cookie"] = f'stok="{self.__auth_code}"'

        if kwargs.get("skip_auth_check"):
            logger.debug("Skipping authentication checks...")
            del kwargs["skip_auth_check"]
        else:
            if not await self.confirm_auth():
                await self.refresh_auth()
                headers["Cookie"] = f'stok="{self.__auth_code}"'

        if method == "GET":
            res = await self.session.get(*args, **kwargs, headers=headers)
        elif method == "POST":
            res = await self.session.post(*args, **kwargs, headers=headers)

        return res

    async def close(self) -> None:
        logger.info("Closign aiohttp client")
        if self.session:
            await self.session.close()
