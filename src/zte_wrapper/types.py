from dataclasses import dataclass
from typing import List, Literal

PhoneNumber = str
RuleType = Literal["TCP"] | Literal["UDP"] | Literal["TCP&UDP"]


class AuthError(Exception):
    pass


@dataclass
class SMSMessage:
    content: str
    tag: int


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
