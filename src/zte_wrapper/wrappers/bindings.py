import json
from typing import List

from ..authwrapper import ZTEAuthWrapper
from ..types import MacBinding


class BindingWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_mac_bindings(self) -> List[MacBinding]:
        data = await self.auth.query_items(["current_static_addr_list"])

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
