from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, TypedDict, Any

PhoneNumber = str
RuleType = Literal["TCP", "UDP", "TCP&UDP"]
InterfaceType = Literal["WIFI6", "WIFI1", "Ethernet", "WIFI", ""]
FirewallProtocolTarget = Literal["TCP", "UDP", "ICMP", "ALL"]
FirewallAction = Literal["DROP", "ACCEPT"]
Hostname = TypedDict("Hostname", {"hostname": str, "mac": str})
AutoOrManual = Literal["auto", "manual"]
SMSRole = Literal["SENT_BY_SELF", "SENT_BY_OTHER", "UNKNOWN"]


class AuthError(Exception):
    pass


class PortRange:
    start: int
    end: int
    iter: int

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __iter__(self):
        self.iter = self.start
        return self

    def __next__(self):
        if self.iter > self.end:
            raise StopIteration

        val = self.iter
        self.iter += 1
        return val

    def as_range(self) -> range:
        return range(self.start, self.end + 1)

    def as_dict(self) -> dict:
        return {"start": self.start, "end": self.end}


@dataclass
class DumbTime:
    year: int
    day: int
    month: int
    hour: int
    minute: int
    second: int
    offset: int


@dataclass
class SMSMessage:
    content: str
    tag: int
    id: int
    date: DumbTime
    mode: SMSRole
    sms_class: int


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
    ports: PortRange
    protocol: RuleType


@dataclass
class PortforwardingTable:
    gateway_addr: str
    enabled: bool
    rules_amount: int
    rules: list[PortforwardingRule]


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
    rules: list[PortmappingRule]


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
        Literal["freedns.afraid.org", "dyndns.org", "zoneedit.org", "no-ip.com"] | str
    )
    account_username: str
    account_password: str
    hash_value: str
    mode: AutoOrManual
    enabled: bool
    domain: str


@dataclass
class MacBinding:
    domain: str | Literal["(null)"]
    hostname: str | Literal["(null)"]
    ip: str
    mac: str


@dataclass
class APNProfile:
    data: str


@dataclass
class APNSettings:
    apn_mode: AutoOrManual
    profile_name: str
    apn_wan_dial: str
    apn_select: AutoOrManual
    pdp_type: Literal["IP"] | str
    pdp_select: AutoOrManual
    pdp_address: str
    index: int
    wan_apn: str
    ppp_auth_mode: str | Literal["none"]
    ppp_username: str
    ppp_password: str
    dns_mode: AutoOrManual
    prefer_dns_manual: str  # find later
    standby_dns_manual: str  # find later x2
    profiles: list[APNProfile]


@dataclass
class DHCPSettings:
    enabled: bool
    end_ip: str
    start_ip: str
    lease_time_hours: int
    dhcp_type: Literal["SERVER"] | str
    lan_ip_addr: str
    lan_netmask: str
    mac_addr: str
    mtu: int
    tcp_mss: int


@dataclass
class FirewallRule:
    mac_addr: str
    source_ip: str
    dest_ip: str
    protocol: FirewallProtocolTarget

    source_port: PortRange
    dest_port: PortRange

    action: FirewallAction
    comment: str


@dataclass
class FirewallConfig:
    default_policy: FirewallAction
    enabled: bool
    rules_ipv4: list[FirewallRule]
    rules_ipv6: list[FirewallRule]


@dataclass
class ChipSettings:
    ap_index: int
    ap_turned_on: bool
    ap_broadcast_disabled: bool
    ap_isolated: bool
    ap_max_devices: int

    authmode: str
    band: str
    bandwidth: int
    channel: int
    chip_index: int
    country_code: str

    current_station_chip_number: int
    encryption_type: str
    guest_ssid_active_time: int
    password: str
    pmf_switch: bool

    ssid: str
    ssid_pmf: str
    wireless_mode: int
