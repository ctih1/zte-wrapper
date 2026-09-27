import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List

from .authwrapper import ZTEAuthWrapper
from .wrappers import (
    apn,
    bindings,
    ddns,
    devices,
    dhcp,
    firewall,
    networktools,
    portforwarding,
    portmapping,
    signal,
    sms,
)

logger = logging.getLogger("zte")


class ZTEWrapper(ZTEAuthWrapper):
    def __init__(self, webui_address: str, password: str) -> None:
        super().__init__(webui_address, password)

        self.portforwarding = portforwarding.PortforwardingWrapper(self)
        self.portmapping = portmapping.PortmappingWrapper(self)
        self.sms = sms.SmsWrapper(self)
        self.signal = signal.SignalWrapper(self)
        self.devices = devices.DeviceWrapper(self)
        self.ddns = ddns.DDNSWrapper(self)
        self.network_tools = networktools.NetworkToolWrapper(self)
        self.bindings = bindings.BindingWrapper(self)
        self.apn = apn.APNWrapper(self)
        self.dhcp = dhcp.DHCPWrapper(self)
        self.firewall = firewall.FirewallWrapper(self)

    async def backup_settings(self) -> dict:
        data = {}

        logger.info("DDNS...")
        data["ddns"] = await self.ddns.get_ddns_settings()

        logger.info("Port forwarding...")
        data["portforw"] = await self.portforwarding.get_port_forwarding_rules()

        logger.info("Port Mapping...")
        data["portmap"] = await self.portmapping.get_portmap_rules()

        logger.info("Bindings...")
        data["bindings"] = await self.bindings.get_mac_bindings()

        logger.info("APN...")
        data["apn"] = await self.apn.get_apn_settings()

        logger.info("DHCP...")
        data["dhcp"] = await self.dhcp.get_settings()

        logger.info("Firewall...")
        data["firewall"] = await self.firewall.get_config()

        return data
