from datetime import datetime

from ..authwrapper import ZTEAuthWrapper
from ..types import Hostname, LanStation, OfflineStation, WirelessStation


class DeviceWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_wlan_station_list(self) -> list[WirelessStation]:
        data = await self.auth.query_items(["station_list"])

        stations: list[WirelessStation] = []

        for station in data["station_list"]:
            stations.append(
                WirelessStation(
                    addr_type=station["addr_type"],
                    connect_time=int(station["connect_time"]),
                    hostname=station["hostname"],
                    interface_type=station["interfacetype"],
                    ip_address=station["ip_addr"],
                    mac_address=station["mac_addr"],
                    mac_bound=station["mac_bind_flag"] == "1",
                    ssid_index=int(station["ssid_index"]),
                    wifi_rssi=int(station["wifi_rssi"]),
                )
            )
        return stations

    async def get_hostnames(self) -> list[Hostname]:
        data = await self.auth.query_items(["hostNameList"])

        return data["devices"]

    async def get_wlan_devices(self) -> list[WirelessStation]:
        """Same as `get_station_list`, but uses the correct hostname

        Returns:
            List[Station]: a list of WiFi devices
        """
        stations = await self.get_wlan_station_list()
        data = await self.get_hostnames()

        for hostname in data:
            target_station: WirelessStation | None = None
            for station in stations:
                if station.mac_address != hostname["mac"]:
                    continue
                target_station = station

            if not target_station:
                continue

            target_station.hostname = hostname["hostname"]

        return stations

    async def get_lan_station_list(self) -> list[LanStation]:
        data = await self.auth.query_items(["lan_station_list"])

        stations: list[LanStation] = []

        for station in data["lan_station_list"]:
            stations.append(
                LanStation(
                    addr_type=station["addr_type"],
                    agreed_rate_mbps=int(station["agreed_rate"]),
                    connect_time=int(station["connect_time"]),
                    hostname=station["hostname"],
                    ip_address=station["ip_addr"],
                    mac_address=station["mac_addr"],
                    mac_bound=station["mac_bind_flag"] == "3",
                )
            )
        return stations

    async def get_lan_devices(self) -> list[LanStation]:
        stations: list[LanStation] = await self.get_lan_station_list()
        data = await self.get_hostnames()

        for hostname in data:
            target_station: LanStation | None = None
            for station in stations:
                if station.mac_address != hostname["mac"]:
                    continue
                target_station = station

            if not target_station:
                continue

            target_station.hostname = hostname["hostname"]

        return stations

    async def get_offline_stations(self) -> list[OfflineStation]:
        data = await self.auth.query_items(["offline_station_list"])
        stations: list[OfflineStation] = []

        for station in data["offline_station_list"]:
            stations.append(
                OfflineStation(
                    hostname=station["hostname"],
                    interface_type=station["interface_type"],
                    ip_address=station["ip_addr"],
                    mac_address=station["mac_addr"],
                    offline_time=datetime.fromtimestamp(int(station["offline_time"])),
                    start_time=datetime.fromtimestamp(int(station["start_time"])),
                    start_time_t=datetime.fromtimestamp(int(station["start_time_t"])),
                )
            )
        return stations

    async def get_offline_devices(self) -> list[OfflineStation]:
        stations: list[OfflineStation] = await self.get_offline_stations()
        data = await self.get_hostnames()

        for hostname in data:
            target_station: OfflineStation | None = None
            for station in stations:
                if station.mac_address != hostname["mac"]:
                    continue
                target_station = station

            if not target_station:
                continue

            target_station.hostname = hostname["hostname"]

        return stations
