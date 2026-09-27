import json

from ..authwrapper import ZTEAuthWrapper
from ..types import DHCPSettings


class DHCPWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_settings(self) -> DHCPSettings:
        data = await self.auth.query_items(
            [
                "lan_ipaddr",
                "lan_netmask",
                "mac_address",
                "dhcpEnabled",
                "dhcpStart",
                "dhcpEnd",
                "dhcpLease_hour",
                "mtu",
                "tcp_mss",
                "lanDhcpType",
            ]
        )

        return DHCPSettings(
            enabled=data["dhcpEnabled"] == "1",
            end_ip=data["dhcpEnd"],
            start_ip=data["dhcpStart"],
            lan_ip_addr=data["lan_ipaddr"],
            lan_netmask=data["lan_netmask"],
            mac_addr=data["mac_address"],
            mtu=int(data["mtu"]),
            tcp_mss=int(data["tcp_mss"]),
            dhcp_type=data["lanDhcpType"] or "SERVER",
            lease_time_hours=int(data["dhcpLease_hour"]),
        )

    async def set_settings(
        self, settings: DHCPSettings, reboot: bool = False
    ) -> tuple[bool, bool]:
        """Updates both DHCP and MTU settings

        Args:
            settings (DHCPSettings): settings object
            reboot (bool, optional): Whether to reboot. Defaults to False.

        Returns:
            Tuple[bool, bool]: whether (DHCP, MTU) settings were applied successfully
        """
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DHCP_SETTING",
                "lanIp": settings.lan_ip_addr,
                "lanNetmask": settings.lan_netmask,
                "lanDhcpType": settings.dhcp_type,
                "dhcpStart": settings.start_ip,
                "dhcpLease": settings.lease_time_hours,
                "dhcp_reboot_flag": int(reboot),
                "mac_ip_reset": "0",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        res2 = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "SET_DEVICE_MTU",
                "mtu": settings.mtu,
                "tcp_mss": settings.tcp_mss,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        data2 = json.loads(await res2.text())
        return (data["result"] == "success", data2["result"] == "success")
