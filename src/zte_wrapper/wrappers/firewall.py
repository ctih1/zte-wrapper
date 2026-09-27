import json
from typing import List, Literal

from ..authwrapper import ZTEAuthWrapper
from ..types import FirewallConfig, FirewallProtocolTarget, FirewallRule, PortRange


class FirewallWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_config(self) -> FirewallConfig:
        data = await self.auth.query_items(
            [
                "IPPortFilterEnable",
                "DefaultFirewallPolicy",
                *[f"IPPortFilterRules_{i}" for i in range(10)],
                *[f"IPPortFilterRulesv6_{i}" for i in range(10)],
            ]
        )

        rules: List[FirewallRule] = []
        rules_ipv6: List[FirewallRule] = []

        for k, v in data.items():
            if k.startswith("IPPortFilterRules") and len(v) > 2:
                (
                    src_ip,
                    _,
                    src_port_start,
                    src_port_end,
                    dest_ip,
                    _,
                    dest_port_start,
                    dest_port_end,
                    protocol,
                    action,
                    comment,
                    mac,
                ) = v.split(",")

                string_protocol: FirewallProtocolTarget | None = None
                i_protocol = int(protocol)

                if i_protocol == 5:
                    string_protocol = "ALL"
                elif i_protocol == 1:
                    string_protocol = "TCP"
                elif i_protocol == 2:
                    string_protocol = "UDP"
                elif i_protocol == 4:
                    string_protocol = "ICMP"

                string_action = "DROP" if action == "1" else "ACCEPT"

                rule = FirewallRule(
                    mac,
                    src_ip,
                    dest_ip,
                    string_protocol or "ALL",
                    PortRange(int(src_port_start), int(src_port_end)),
                    PortRange(int(dest_port_start), int(dest_port_end)),
                    string_action,
                    comment,
                )

                if k.startswith("IPPortFilterRulesv6_"):
                    rules_ipv6.append(rule)
                else:
                    rules.append(rule)

        return FirewallConfig(
            default_policy="ACCEPT" if data["DefaultFirewallPolicy"] == "0" else "DROP",
            enabled=data["IPPortFilterEnable"] == "1",
            rules_ipv4=rules,
            rules_ipv6=rules_ipv6,
        )

    async def delete_rules(
        self,
        rule_ipv4_indices: List[int] | None = None,
        rule_ipv6_indices: List[int] | None = None,
    ) -> bool:
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "DEL_IP_PORT_FILETER_V4V6",
                "delete_id": (
                    ""
                    if not rule_ipv4_indices
                    else ";".join([str(r) for r in rule_ipv4_indices]) + ";"
                ),
                "delete_id_v6": (
                    ""
                    if not rule_ipv6_indices
                    else ";".join([str(r) for r in rule_ipv6_indices]) + ";"
                ),
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        return data["result"] == "success"

    async def add_rule(
        self, ip_type: Literal["ipv4", "ipv6"], rule: FirewallRule
    ) -> bool:
        d = {
            "isTest": "false",
            "goformId": "ADD_IP_PORT_FILETER_V4V6",
            "ip_version": ip_type,
            "mac_address": rule.mac_addr,
            "dip_address": rule.dest_ip,
            "sip_address": rule.source_ip,
            "dFromPort": rule.dest_port.start,
            "dToPort": rule.dest_port.end,
            "sFromPort": rule.source_port.start,
            "sToPort": rule.source_port.end,
            "action": rule.action.capitalize(),
            "protocol": "None" if rule.protocol == "ALL" else rule.protocol,
            "comment": rule.comment,
            "AD": await self.auth.construct_ad_token(),
        }
        print(d)
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data=d,
        )

        data = json.loads(await res.text())
        return data["result"] == "success"
