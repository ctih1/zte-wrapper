import json
from typing import Dict, List
from .authwrapper import ZTEAuthWrapper
from .types import (
    SMSMessage,
    PhoneNumber,
    AuthError,
    SignalStrength,
    NetworkDetails,
    PortforwardingRule,
    PortforwardingTable,
    RuleType,
)


def utf_16_decode(inp: str) -> str:
    return bytes.fromhex(inp).decode("utf-16-be")


class ZTEWrapper(ZTEAuthWrapper):
    def __init__(self, webui_address: str, password: str) -> None:
        super().__init__(webui_address, password)

    async def get_port_forwarding_rules(self) -> PortforwardingTable:
        res = await self.request(
            "GET",
            self.construct_url(
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

    async def set_portforwarding_rule(self, rule: PortforwardingRule) -> None:
        res = await self.request(
            "POST",
            self.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "FW_FORWARD_ADD",
                "ipAddress": rule.ip_addr,
                "portStart": rule.port_start,
                "portEnd": rule.port_end,
                "protocol": rule.protocol,
                "comment": rule.comment,
                "AD": await self.construct_ad_token(),
            },
        )

        print(json.dumps(json.loads(await res.text()), indent=4))

    async def get_sms(self) -> Dict[PhoneNumber, List[SMSMessage]]:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "sms_data_total",
                    "page": "0",
                    "data_per_page": "1500",
                    "mem_store": "1",
                    "tags": "10",
                    "order_by": "order by id desc",
                    "_": self.get_timestamp(),
                },
            ),
        )

        jason = json.loads(await res.text())

        if jason.get("sms_data_total") == "" or jason.get("messages") is None:
            raise AuthError("Failed to retrieve data from SMS")

        results: Dict[PhoneNumber, List[SMSMessage]] = {}
        for message in jason["messages"]:
            phone_number = utf_16_decode(message["number"])

            if phone_number not in results:
                results[phone_number] = []

            results[phone_number].append(
                SMSMessage(
                    content=utf_16_decode(message["content"]), tag=int(message["tag"])
                )
            )

        return results

    async def get_signal_strength(self) -> SignalStrength:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "Z5g_SINR,Z5g_rsrp,Z5g_rsrq,Z5g_rssi,lte_pci,lte_rsrq,lte_rssi,lte_snr,network_Z5g_CELLINFO_band,network_ZCELLINFO_band,network_lte_rsrp",
                    "multi_data": "1",
                    "_": self.get_timestamp(),
                },
            ),
        )

        jason = json.loads(await res.text())

        return SignalStrength(
            sinr_5g=float(jason["Z5g_SINR"]),
            rsrp_5g=float(jason["Z5g_rsrp"]),
            rsrq_5g=float(jason["Z5g_rsrq"]),
            rssi_5g=float(jason["Z5g_rssi"]),
            band_5g=jason["network_Z5g_CELLINFO_band"],
            band_lte=jason["network_ZCELLINFO_band"],
            pci_lte=float(jason["lte_pci"]),
            rsrq_lte=float(jason["lte_rsrq"]),
            rsrp_lte=float(jason["network_lte_rsrp"]),
            rssi_lte=float(jason["lte_rssi"]),
            snr_lte=float(jason["lte_snr"]),
        )

    async def get_network_details(self) -> NetworkDetails:
        res = await self.request(
            "GET",
            self.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "network_provider_fullname,flux_realtime_tx_thrpt,flux_realtime_rx_thrpt,flux_monthly_tx_bytes,flux_monthly_rx_bytes",
                    "multi_data": "1",
                    "_": self.get_timestamp(),
                },
            ),
        )

        jason = json.loads(await res.text())

        return NetworkDetails(
            isp_name=jason["network_provider_fullname"],
            download_mbps=(float(jason["flux_realtime_rx_thrpt"]) * 8) / (1024 * 1024),
            upload_mbps=(float(jason["flux_realtime_tx_thrpt"]) * 8) / (1024 * 1024),
            monthly_download_megabytes=float(jason["flux_monthly_rx_bytes"])
            / (1024 * 1024),
            monthly_upload_megabytes=float(jason["flux_monthly_tx_bytes"])
            / (1024 * 1024),
        )
