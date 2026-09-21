from ..authwrapper import ZTEAuthWrapper
import json
from ..types import PortmappingRule, PortmappingTable, RuleType
from typing import List


class PortmappingWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_portmap_rules(self) -> PortmappingTable:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "lan_ipaddr,PortMapEnable,portmap_rule_num,PortMapRules_0,PortMapRules_1,PortMapRules_2,PortMapRules_3,PortMapRules_4,PortMapRules_5,PortMapRules_6,PortMapRules_7,PortMapRules_8,PortMapRules_9,PortMapRules_10,PortMapRules_11,PortMapRules_12,PortMapRules_13,PortMapRules_14,PortMapRules_15,PortMapRules_16,PortMapRules_17,PortMapRules_18,PortMapRules_19,PortMapRules_20,PortMapRules_21,PortMapRules_22,PortMapRules_23,PortMapRules_24,PortMapRules_25,PortMapRules_26,PortMapRules_27,PortMapRules_28,PortMapRules_29,PortMapRules_30,PortMapRules_31",
                    "multi_data": "1",
                },
            ),
        )

        data: dict = json.loads(await res.text())
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
