from ..authwrapper import ZTEAuthWrapper
import json
from ..types import PortforwardingRule, PortforwardingTable, RuleType
from typing import List


class PortforwardingWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_port_forwarding_rules(self) -> PortforwardingTable:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "lan_ipaddr,PortForwardEnable,portforward_rule_num,PortForwardRules_0,PortForwardRules_1,PortForwardRules_2,PortForwardRules_3,PortForwardRules_4,PortForwardRules_5,PortForwardRules_6,PortForwardRules_7,PortForwardRules_8,PortForwardRules_9,PortForwardRules_10,PortForwardRules_11,PortForwardRules_12,PortForwardRules_13,PortForwardRules_14,PortForwardRules_15,PortForwardRules_16,PortForwardRules_17,PortForwardRules_18,PortForwardRules_19,PortForwardRules_20,PortForwardRules_21,PortForwardRules_22,PortForwardRules_23,PortForwardRules_24,PortForwardRules_25,PortForwardRules_26,PortForwardRules_27,PortForwardRules_28,PortForwardRules_29",
                    "multi_data": "1",
                },
            ),
        )

        data: dict = json.loads(await res.text())
        rules: List[PortforwardingRule] = []

        for k, v in data.items():
            k: str = k
            v: str = str(v)

            if k.startswith("PortForwardRules_") and len(v) != 0:
                ip, from_port, to_port, protocol_int_str, comment = v.split(",")
                protocol_int: int = int(protocol_int_str)
                protocol: RuleType = "TCP&UDP"
                if protocol_int == 1:
                    protocol = "TCP"
                elif protocol_int == 2:
                    protocol = "UDP"

                rules.append(
                    PortforwardingRule(
                        ip_addr=ip,
                        comment=comment,
                        port_start=int(from_port),
                        port_end=int(to_port),
                        protocol=protocol,
                    )
                )

        return PortforwardingTable(
            gateway_addr=data["lan_ipaddr"],
            enabled=data["PortForwardEnable"] == "1",
            rules_amount=int(data["portforward_rule_num"]),
            rules=rules,
        )

    async def set_portforwarding_rule(self, rule: PortforwardingRule) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "FW_FORWARD_ADD",
                "ipAddress": rule.ip_addr,
                "portStart": rule.port_start,
                "portEnd": rule.port_end,
                "protocol": rule.protocol,
                "comment": rule.comment,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def delete_portforwarding_rules(self, indices: List[int]) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "FW_FORWARD_DEL",
                "delete_id": ";".join([str(i) for i in indices]) + ";",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
