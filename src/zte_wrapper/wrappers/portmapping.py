import json
from typing import List

from ..authwrapper import ZTEAuthWrapper
from ..types import PortmappingRule, PortmappingTable, RuleType


class PortmappingWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_portmap_rules(self) -> PortmappingTable:
        data = await self.auth.query_items(
            [
                "lan_ipaddr",
                "PortMapEnable",
                "portmap_rule_num",
                *[f"PortMapRules_{i}" for i in range(30)],
            ]
        )

        rules: List[PortmappingRule] = []

        for k, v in data.items():
            k: str = k
            v: str = str(v)

            if k.startswith("PortMapRules_") and len(v) != 0:
                ip, ext_port, int_port, protocol_int_str, comment = v.split(",")
                protocol_int: int = int(protocol_int_str)
                protocol: RuleType = "TCP&UDP"
                if protocol_int == 1:
                    protocol = "TCP"
                elif protocol_int == 2:
                    protocol = "UDP"

                rules.append(
                    PortmappingRule(
                        ip_addr=ip,
                        comment=comment,
                        port_external=int(ext_port),
                        port_internal=int(int_port),
                        protocol=protocol,
                    )
                )

        return PortmappingTable(
            gateway_addr=data["lan_ipaddr"],
            enabled=data["PortMapEnable"] == "1",
            rules_amount=int(data["portmap_rule_num"]),
            rules=rules,
        )

    async def set_portmap_rule(self, rule: PortmappingRule) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "ADD_PORT_MAP",
                "portMapEnabled": "1",
                "ipAddress": rule.ip_addr,
                "fromPort": rule.port_external,
                "toPort": rule.port_internal,
                "protocol": rule.protocol,
                "comment": rule.comment,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def delete_portmapping_rules(self, indices: List[int]) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DEL_PORT_MAP",
                "delete_id": ";".join([str(i) for i in indices]) + ";",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
