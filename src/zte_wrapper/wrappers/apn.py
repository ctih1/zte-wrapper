import json
from typing import List

from ..authwrapper import ZTEAuthWrapper
from ..types import APNProfile, APNSettings


class APNWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_apn_settings(self) -> APNSettings:
        data = await self.auth.query_items(
            [
                "apn_interface_version",
                *[f"APN_config{i}" for i in range(20)],
                *[f"ipv6_APN_config{i}" for i in range(20)],
                "profile_name",
                "apn_wan_dial",
                "apn_select",
                "apn_pdp_type",
                "apn_pdp_select",
                "apn_pdp_addr",
                "index",
                "apn_Current_index",
                "apn_mode",
                "apn_wan_apn",
                "apn_ppp_auth_mode",
                "apn_ppp_username",
                "apn_ppp_passwd",
                "dns_mode",
                "prefer_dns_manual",
                "standby_dns_manual",
                "profile_name_ui",
                "pdp_type_ui",
                "ppp_auth_mode_ui",
                "ppp_username_ui",
                "ppp_passwd_ui",
                "dns_mode_ui",
            ]
        )

        profiles: List[APNProfile] = []

        for k, v in data.items():
            if k.startswith(("ipv6_APN_config", "APN_config")):
                profiles.append(APNProfile(data=v))

        settings = APNSettings(
            apn_mode=data["apn_mode"],
            apn_select=data["apn_select"],
            apn_wan_dial="*99#",
            dns_mode=data["dns_mode"],
            pdp_address=data["apn_pdp_addr"],
            pdp_select="auto",
            pdp_type=data["apn_pdp_type"],
            ppp_auth_mode=data["apn_ppp_auth_mode"],
            ppp_password=data["apn_ppp_passwd"],
            ppp_username=data["apn_ppp_username"],
            prefer_dns_manual=data["prefer_dns_manual"],
            profile_name=data["profile_name_ui"],
            standby_dns_manual=data["standby_dns_manual"],
            wan_apn=data["apn_wan_apn"],
            index=int(data["apn_Current_index"]),
            profiles=profiles,
        )
        return settings

    async def set_apn_settings(self, settings: APNSettings) -> bool:
        d = {
            "isTest": "false",
            "goformId": "APN_PROC_EX",
            "apn_action": "save",
            "apn_mode": settings.apn_mode,
            "profile_name": settings.profile_name,
            "apn_wan_dial": settings.apn_wan_dial,
            "apn_select": settings.apn_select,
            "apn_pdp_type": settings.pdp_type,
            "apn_pdp_select": settings.pdp_select,
            "apn_pdp_addr": settings.pdp_address,
            "index": str(settings.index),
            "apn_wan_apn": settings.wan_apn,
            "apn_ppp_auth_mode": settings.ppp_auth_mode,
            "apn_ppp_username": settings.ppp_username,
            "apn_ppp_passwd": settings.ppp_password,
            "dns_mode": settings.dns_mode,
            "prefer_dns_manual": settings.prefer_dns_manual,
            "standby_dns_manual": settings.standby_dns_manual,
            "AD": await self.auth.construct_ad_token(),
        }
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data=d,
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
