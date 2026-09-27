import base64

from ..authwrapper import ZTEAuthWrapper
from ..types import ChipSettings


class WiFiWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_settings(self) -> list[ChipSettings]:
        stations = await self.auth.query_items(["queryAccessPointInfo"])

        chip_settings: list[ChipSettings] = []

        for station in stations["ResponseList"]:
            if station["AccessPointSwitchStatus"] == "":
                continue

            chip_settings.append(
                ChipSettings(
                    ap_broadcast_disabled=station["ApBroadcastDisabled"] == "1",
                    ap_index=int(station["AccessPointIndex"]),
                    ap_isolated=station["ApIsolate"] == "1",
                    ap_max_devices=int(station["ApMaxStationNumber"]),
                    ap_turned_on=station["AccessPointSwitchStatus"] == "1",
                    authmode=station["AuthMode"],
                    band=station["Band"],
                    bandwidth=station["BandWidth"],
                    channel=station["Channel"],
                    chip_index=int(station["ChipIndex"]),
                    country_code=station["CountryCode"],
                    current_station_chip_number=int(station["CurrentStationNumber"]),
                    encryption_type=station["EncrypType"],
                    guest_ssid_active_time=int(station["GuestSSIDActiveTime"] or "-1"),
                    password=base64.b64decode(station["Password"]).decode("UTF-8"),
                    pmf_switch=station["Pmf_switch"],
                    ssid=station["SSID"],
                    ssid_pmf=station["SSIDPMF"],
                    wireless_mode=int(station["WirelessMode"]),
                )
            )

        return chip_settings
