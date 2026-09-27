from ..authwrapper import ZTEAuthWrapper
import json
from ..types import APNSettings, APNProfile
from typing import List


class APNWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_apn_settings(self) -> APNSettings:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "cmd": "apn_interface_version,APN_config0,APN_config1,APN_config2,APN_config3,APN_config4,APN_config5,APN_config6,APN_config7,APN_config8,APN_config9,APN_config10,APN_config11,APN_config12,APN_config13,APN_config14,APN_config15,APN_config16,APN_config17,APN_config18,APN_config19,ipv6_APN_config0,ipv6_APN_config1,ipv6_APN_config2,ipv6_APN_config3,ipv6_APN_config4,ipv6_APN_config5,ipv6_APN_config6,ipv6_APN_config7,ipv6_APN_config8,ipv6_APN_config9,ipv6_APN_config10,ipv6_APN_config11,ipv6_APN_config12,ipv6_APN_config13,ipv6_APN_config14,ipv6_APN_config15,ipv6_APN_config16,ipv6_APN_config17,ipv6_APN_config18,ipv6_APN_config19,apn_m_profile_name,profile_name,apn_wan_dial,apn_select,apn_pdp_type,apn_pdp_select,apn_pdp_addr,index,apn_Current_index,apn_auto_config,apn_ipv6_apn_auto_config,apn_mode,apn_wan_apn,apn_ppp_auth_mode,apn_ppp_username,apn_ppp_passwd,dns_mode,prefer_dns_manual,standby_dns_manual,apn_ipv6_wan_apn,apn_ipv6_pdp_type,apn_ipv6_ppp_auth_mode,apn_ipv6_ppp_username,apn_ipv6_ppp_passwd,ipv6_dns_mode,ipv6_prefer_dns_manual,ipv6_standby_dns_manual,apn_num_preset,wan_apn_ui,profile_name_ui,pdp_type_ui,ppp_auth_mode_ui,ppp_username_ui,ppp_passwd_ui,dns_mode_ui,prefer_dns_manual_ui,standby_dns_manual_ui,ipv6_wan_apn_ui,ipv6_ppp_auth_mode_ui,ipv6_ppp_username_ui,ipv6_ppp_passwd_ui,ipv6_dns_mode_ui,ipv6_prefer_dns_manual_ui,ipv6_standby_dns_manual_ui",
                    "isTest": "false",
                    "multi_data": "1",
                },
            ),
        )

        data: dict = json.loads(await res.text())
        profiles: List[APNProfile] = []

        for k, v in data.items():
            k: str = k
            v: str = v

            if k.startswith("ipv6_APN_config") or k.startswith("APN_config"):
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
