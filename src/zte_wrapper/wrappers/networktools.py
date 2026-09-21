from ..authwrapper import ZTEAuthWrapper
import json
from ..types import PortforwardingRule, PortforwardingTable, RuleType
from typing import List


class NetworkToolWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def start_ping(
        self, target: str, ping_count: int = 5, packet_size: int = 64
    ) -> bool:
        """Starts pinging specific IP address or domain. To get the output, poll `get_ping_output` until it returns a value.

        Args:
            target (str): IP address or domain to ping
            ping_count (int, optional): How many times to ping. Defaults to 5.
            packet_size (int, optional): How many bytes is the packet. Defaults to 64.

        Returns:
            bool: whether the ping started.
        """
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DIAGLOG",
                "DIAG_URL": target,
                "DIAG_CHECK": "0",
                "ping_count": ping_count,
                "ping_type": "4",
                "ping_quiet": "1",
                "ping_size": packet_size,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def get_ping_output(self) -> str:
        await self.clear_ping_output()

        res = await self.auth.request(
            "GET",
            f"http://{self.auth.address}/PingMessages?_={self.auth.get_timestamp()}",
        )

        return await res.text()

    async def clear_ping_output(self) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DIAGLOG",
                "DIAG_CHECK": "0",
                "diag_del_action": "0",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def start_traceroute(self, target: str) -> bool:
        """Starts tracerouting to specific IP address or domain. To get the output, poll `get_traceroute_output` until it returns a value.

        Args:
            target (str): IP address or domain to ping

        Returns:
            bool: whether the traceroute started.
        """
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DIAGLOG",
                "DIAG_URL": target,
                "DIAG_CHECK": "1",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def get_traceroute_output(self) -> str:
        await self.clear_traceroute_output()

        res = await self.auth.request(
            "GET",
            f"http://{self.auth.address}/TracerouteMessages?_={self.auth.get_timestamp()}",
        )

        return await res.text()

    async def clear_traceroute_output(self) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DIAGLOG",
                "DIAG_CHECK": "1",
                "diag_del_action": "0",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def reboot_router(self) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "REBOOT_DEVICE",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
