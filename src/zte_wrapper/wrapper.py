import json
from typing import Dict, List
from .authwrapper import ZTEAuthWrapper
from .types import SMSMessage, PhoneNumber, AuthError, SignalStrength


def utf_16_decode(inp: str) -> str:
    return bytes.fromhex(inp).decode("utf-16-be")


class ZTEWrapper(ZTEAuthWrapper):
    def __init__(self, webui_address: str, password: str) -> None:
        super().__init__(webui_address, password)

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

        print(json.dumps(jason, indent=4))
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
        print(jason)

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
