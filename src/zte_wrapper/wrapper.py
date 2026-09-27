import json
from typing import Dict, List
from datetime import datetime
from .authwrapper import ZTEAuthWrapper
from .wrappers import (
    portforwarding,
    sms,
    signal,
    devices,
    portmapping,
    ddns,
    networktools,
    bindings,
    apn,
    dhcp,
)


class ZTEWrapper(ZTEAuthWrapper):
    def __init__(self, webui_address: str, password: str) -> None:
        super().__init__(webui_address, password)

        self.portforwarding = portforwarding.PortforwardingWrapper(self)
        self.portmapping = portmapping.PortmappingWrapper
        self.sms = sms.SmsWrapper(self)
        self.signal = signal.SignalWrapper(self)
        self.devices = devices.DeviceWrapper(self)
        self.ddns = ddns.DDNSWrapper(self)
        self.network_tools = networktools.NetworkToolWrapper(self)
        self.bindings = bindings.BindingWrapper(self)
        self.apn = apn.APNWrapper(self)
        self.dhcp = dhcp.DHCPWrapper(self)

    async def perform_dbg_query(self, items: List[str]) -> dict:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {"cmd": ",".join(items), "isTest": "false", "multi_data": "true"},
            ),
        )

        txt = await res.text()
        try:
            data = json.loads(txt)
            return data
        except Exception as e:
            print(txt)
            print(e)
            return {}
