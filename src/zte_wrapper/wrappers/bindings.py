from ..authwrapper import ZTEAuthWrapper
import json
from ..types import MacBinding
from typing import List


class BindingWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_mac_bindings(self) -> List[MacBinding]:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "current_static_addr_list",
                },
            ),
        )

        data: dict = json.loads(await res.text())
        bindings: List[MacBinding] = []

        for binding in data["current_static_addr_list"]:
            bindings.append(
                MacBinding(
                    domain=binding["domain"],
                    hostname=binding["hostname"],
                    ip=binding["ip"],
                    mac=binding["mac"],
                )
            )

        return bindings

    async def create_mac_binding(self, mac_address: str, ip: str) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "BIND_STATIC_ADDRESS_ADD",
                "mac_address": mac_address,
                "ip_address": ip,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def delete_mac_binding(self, mac_address: str) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "BIND_STATIC_ADDRESS_DEL",
                "mac_address": mac_address,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
