from dataclasses import dataclass
from typing import List, Literal, TypedDict
from datetime import datetime

PhoneNumber = str
RuleType = Literal["TCP"] | Literal["UDP"] | Literal["TCP&UDP"]
InterfaceType = (
    Literal["WIFI6"]
    | Literal["WIFI1"]
    | Literal["Ethernet"]
    | Literal["WIFI"]
    | Literal[""]
)
Hostname = TypedDict("Hostname", {"hostname": str, "mac": str})


class AuthError(Exception):
    pass


@dataclass
class SMSMessage:
    content: str
    tag: int
    id: int


@dataclass
class SignalStrength:
    sinr_5g: float
    rsrp_5g: float
    rsrq_5g: float
    rssi_5g: float

    band_5g: str
    band_lte: str

    pci_lte: float
    rsrq_lte: float
    rsrp_lte: float
    rssi_lte: float
    snr_lte: float


@dataclass
class NetworkDetails:
    isp_name: str
    download_mbps: float
    upload_mbps: float
    monthly_download_megabytes: float
    monthly_upload_megabytes: float


@dataclass
class PortforwardingRule:
    ip_addr: str
    comment: str
    port_start: int
    port_end: int
    protocol: RuleType


@dataclass
class PortforwardingTable:
    gateway_addr: str
    enabled: bool
    rules_amount: int
    rules: List[PortforwardingRule]


@dataclass
class PortmappingRule:
    ip_addr: str
    comment: str
    port_external: int
    port_internal: int
    protocol: RuleType


@dataclass
class PortmappingTable:
    gateway_addr: str
    enabled: bool
    rules_amount: int
    rules: List[PortmappingRule]


@dataclass
class WirelessStation:  # basically a wireless device
    addr_type: Literal["DHCP"] | str
    connect_time: int
    hostname: str
    interface_type: InterfaceType
    ip_address: str
    mac_address: str
    mac_bound: bool
    ssid_index: int
    wifi_rssi: int


@dataclass
class LanStation:
    addr_type: Literal["Static"] | str
    agreed_rate_mbps: int
    connect_time: int
    hostname: str
    ip_address: str
    mac_address: str
    mac_bound: bool


@dataclass
class OfflineStation:
    interface_type: InterfaceType
    offline_time: datetime
    start_time: datetime
    start_time_t: datetime
    hostname: str
    ip_address: str
    mac_address: str


@dataclass
class DDNSSettings:
    provider: (
        Literal["freedns.afraid.org"]
        | Literal["dyndns.org"]
        | Literal["zoneedit.org"]
        | Literal["no-ip.com"]
        | str
    )
    account_username: str
    account_password: str
    hash_value: str
    mode: Literal["auto"] | Literal["manual"]
    enabled: bool
    domain: str


@dataclass
class MacBinding:
    domain: str | Literal["(null)"]
    hostname: str | Literal["(null)"]
    ip: str
    mac: str
