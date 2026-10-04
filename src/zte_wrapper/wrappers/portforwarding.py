import json

from ..authwrapper import ZTEAuthWrapper
from ..types import PortforwardingRule, PortforwardingTable, PortRange, RuleType


class PortforwardingWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_port_forwarding_rules(self) -> PortforwardingTable:
        data = await self.auth.query_items(
            [
                "lan_ipaddr",
                "PortForwardEnable",
                "portforward_rule_num",
                *[f"PortForwardRules_{i}" for i in range(30)],
            ]
        )

        rules: list[PortforwardingRule] = []

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
                        ports=PortRange(int(from_port), int(to_port)),
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
                "portStart": rule.ports.start,
                "portEnd": rule.ports.end,
                "protocol": rule.protocol,
                "comment": rule.comment,
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def delete_portforwarding_rules(self, indices: list[int]) -> bool:
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
