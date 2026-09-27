import json
from typing import List

from ..authwrapper import ZTEAuthWrapper
from ..types import DDNSSettings


class DDNSWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_ddns_settings(self) -> DDNSSettings:
        data = await self.auth.query_items(
            [
                "DDNS_Enable",
                "DDNS_Mode",
                "DDNSProvider",
                "DDNSAccount",
                "DDNSPassword",
                "DDNS",
                "DDNS_Hash_Value",
            ]
        )
        return DDNSSettings(
            provider=data["DDNSProvider"],
            enabled=data["DDNS_Enable"] == "1",
            mode=data["DDNS_Mode"],
            account_username=data["DDNSAccount"],
            account_password=data["DDNSPassword"],
            hash_value=data["DDNS_Hash_Value"],
            domain=data["DDNS"],
        )

    async def update_ddns(self, settings: DDNSSettings) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DDNS",
                "DDNS_Enable": "1" if settings.enabled else "0",
                "DDNS_Mode": settings.mode,
                "DDNSProvider": settings.provider,
                "DDNS": settings.domain,
                "DDNSAccount": settings.account_username,
                "DDNSPassword": settings.account_password,
                "DDNS_Hash_Value": settings.hash_value,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
